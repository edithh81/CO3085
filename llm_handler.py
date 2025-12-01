import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from typing import List, Dict

class LLMHandler:
    def __init__(self, model_name: str = "vilm/vinallama-7b-chat"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load only vinallama-7b-chat
        model_to_load = "vilm/vinallama-7b-chat"
        
        self.model = None
        self.tokenizer = None
        
        try:
            print(f"Loading: {model_to_load}")
            self.model, self.tokenizer = self._load_model(model_to_load)
            self.current_model = model_to_load
            print(f"✓ Successfully loaded: {model_to_load}")
        except Exception as e:
            raise RuntimeError(f"Failed to load {model_to_load}: {str(e)}")
        
        print("Model loaded successfully!")
    
    def _load_model(self, model_name: str):
        """Load model with appropriate configuration"""
        # 4-bit quantization config for 4GB VRAM
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        
        # Set pad token if not exists
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load model with quantization
        if self.device == "cuda":
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=quantization_config,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.float16
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                trust_remote_code=True
            )
        
        return model, tokenizer
    
    def generate_response(self, prompt: str, max_length: int = 200) -> str:
        """Generate response from LLM with proper cleaning"""
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        ).to(self.device)
        
        input_length = inputs['input_ids'].shape[1]
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.2,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        generated_tokens = outputs[0]
        response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
        
        print("Generated Response:", response)
        
        # Clean the response
        return self._clean_response(response)
    
    def _clean_response(self, response: str) -> str:
        """Clean the generated response"""
        response = response.strip()
        # just take the last assistant response
        response_parts = response.rfind("assistant")
        print("Response parts index:", response_parts)
        if response_parts != -1:
            response = response[response_parts + len("assistant"):].strip()
        else:
            response = "Xin lỗi, tôi chưa hiểu rõ yêu cầu của bạn."
        
        return response.strip()

    def create_prompt(self, context: str, query: str, chat_history: List[Dict]) -> str:
        """Create simplified prompt - system context in one block"""
        # Combine system prompt and context into one message
        system_message = "Bạn là trợ lý nhà hàng. Trả lời ngắn gọn về món ăn, giá cả, đặt món."
        
        # Build prompt
        prompt = f"<|im_start|> system\n{system_message}<|im_end|>\n"
        
        # Add only the last turn of history (if exists)
        if chat_history and len(chat_history) > 0:
            last_turn = chat_history[-1]
            prompt += f"<|im_start|> user\n{last_turn['user']}<|im_end|>\n"
            prompt += f"<|im_start|> assistant\n{last_turn['assistant']}<|im_end|>\n"
        
        # Add current query
        prompt += f"<|im_start|> user\n{query}<|im_end|>\n"
        prompt += "<|im_start|> assistant\n"
        
        return prompt
    
    def get_welcome_message(self) -> str:
        """Return default welcome message without LLM generation"""
        # Always use default message for consistency and speed
        return self._default_welcome()
    
    def _default_welcome(self) -> str:
        """Default welcome message"""
        return """Xin chào! Tôi là trợ lý ảo của nhà hàng. 🍜

Tôi có thể giúp bạn:
• 📋 Xem menu và thông tin món ăn
• 🛒 Đặt món và quản lý giỏ hàng
• ✅ Xác nhận đơn hàng
• ❌ Hủy đơn hàng

Bạn muốn xem menu hay đặt món gì ạ?"""
