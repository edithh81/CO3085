import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from typing import List, Dict

class LLMHandler:
    def __init__(self, model_name: str = "vilm/vinallama-2.7b-chat"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Focus on vinallama-2.7b-chat
        model_candidates = [
            "vilm/vinallama-2.7b-chat",  # Primary Vietnamese model
            "Qwen/Qwen2-1.5B-Instruct",  # Fallback
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Last resort
        ]
        
        if model_name and model_name not in model_candidates:
            model_candidates.insert(0, model_name)
        
        self.model = None
        self.tokenizer = None
        
        # Try loading models in order
        for candidate in model_candidates:
            try:
                print(f"Attempting to load: {candidate}")
                self.model, self.tokenizer = self._load_model(candidate)
                self.current_model = candidate
                print(f"✓ Successfully loaded: {candidate}")   
                break
            except Exception as e:
                print(f"✗ Failed to load {candidate}: {str(e)[:100]}")
                continue
        
        if self.model is None:
            raise RuntimeError("Failed to load any LLM model. Check your internet connection and GPU memory.")
        
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
    
    def generate_response(self, prompt: str, max_length: int = 256) -> str:
        """Generate response from LLM"""
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            truncation=True,
            max_length=1024
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                top_p=0.9,
                top_k=50,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part
        response = self._clean_response(response, prompt)
        
        return response
    
    def _clean_response(self, response: str, prompt: str) -> str:
        """Clean and extract the actual response - only take last assistant response"""
        # Remove the prompt from response
        if prompt in response:
            response = response.replace(prompt, "").strip()
        
        # Split by assistant marker and take only the LAST response
        if "<|im_start|>assistant" in response:
            parts = response.split("<|im_start|>assistant")
            response = parts[-1].strip()  # Take only the last assistant response
        
        # Remove end markers
        if "<|im_end|>" in response:
            response = response.split("<|im_end|>")[0].strip()
        
        # Clean up any remaining markers
        response = response.replace("<|im_start|>user", "").strip()
        response = response.replace("<|im_start|>system", "").strip()
        
        # Remove repeated lines
        lines = response.split('\n')
        unique_lines = []
        seen = set()
        for line in lines:
            line = line.strip()
            if line and line not in seen:
                unique_lines.append(line)
                seen.add(line)
        
        response = '\n'.join(unique_lines)
        
        # Limit length if too long
        if len(response) > 400:
            sentences = [s.strip() for s in response.split('.') if s.strip()]
            response = '. '.join(sentences[:3]) + '.'
        
        return response.strip()
    
    def create_prompt(self, context: str, query: str, chat_history: List[Dict]) -> str:
        """Create straightforward prompt using vinallama chat template"""
        # Simplified system prompt
        system_prompt = """Bạn là trợ lý nhà hàng. Trả lời ngắn gọn, rõ ràng về: món ăn, giá, đặt món, hủy món."""

        # Start with system message
        prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        
        # Add context if available (keep it concise)
        if context:
            prompt += f"<|im_start|>system\nMenu: {context}<|im_end|>\n"
        
        # Only add last conversation turn (not multiple history)
        if chat_history and len(chat_history) > 0:
            last_turn = chat_history[-1]
            prompt += f"<|im_start|>user\n{last_turn['user']}<|im_end|>\n"
            prompt += f"<|im_start|>assistant\n{last_turn['assistant']}<|im_end|>\n"
        
        # Add current query
        prompt += f"<|im_start|>user\n{query}<|im_end|>\n"
        prompt += "<|im_start|>assistant\n"
        
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
