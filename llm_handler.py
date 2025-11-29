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
    
    def _clean_response(self, response: str, prompt: str) -> str:
        """Clean and extract the actual response - more robust approach"""
        # Method 1: If we find the assistant marker, extract everything after the last one
        if "<|im_start|>assistant" in response:
            parts = response.split("<|im_start|>assistant")
            response = parts[-1].strip()
        
        # Method 2: If no marker but prompt exists, remove prompt
        elif prompt in response:
            response = response.replace(prompt, "").strip()
        
        # Method 3: If response starts with assistant text after prompt removal
        assistant_markers = ["<|im_start|>assistant", "assistant"]
        for marker in assistant_markers:
            if response.startswith(marker):
                response = response[len(marker):].strip()
        
        # Remove end markers and other special tokens
        end_markers = ["<|im_end|>", "<|endoftext|>", "</s>"]
        for marker in end_markers:
            if marker in response:
                response = response.split(marker)[0].strip()
        
        # Clean up any remaining chat markers
        chat_markers = ["<|im_start|>user", "<|im_start|>system", "user:", "system:"]
        for marker in chat_markers:
            response = response.replace(marker, "").strip()
        
        # Remove duplicate lines while preserving order
        lines = []
        seen = set()
        for line in response.split('\n'):
            line_clean = line.strip()
            if line_clean and line_clean not in seen:
                lines.append(line_clean)
                seen.add(line_clean)
        
        response = '\n'.join(lines)
        
        # Smart length limiting - don't cut in middle of sentences
        if len(response) > 400:
            # Try to cut at sentence boundaries
            sentences = []
            current = ""
            for char in response:
                current += char
                if char in '.!?。！？' and len(current) > 20:
                    sentences.append(current.strip())
                    current = ""
                    if sum(len(s) for s in sentences) > 350:
                        break
            if sentences:
                response = ' '.join(sentences)
            else:
                # Fallback: cut at word boundary
                response = response[:397] + "..."
        
        return response.strip()

    def create_prompt(self, context: str, query: str, chat_history: List[Dict]) -> str:
        """Create optimized prompt for Vietnamese models"""
        # Vietnamese system prompt
        system_prompt = """Bạn là trợ lý AI cho nhà hàng. Hãy trả lời câu hỏi về thực đơn, giá cả, đặt món và các dịch vụ nhà hàng một cách ngắn gọn, chính xác và hữu ích."""
        
        prompt_parts = []
        
        # System message
        prompt_parts.append(f"<|im_start|>system\n{system_prompt}<|im_end|>")
        
        # Add context if available
        if context:
            prompt_parts.append(f"<|im_start|>system\nThông tin thực đơn: {context}<|im_end|>")
        
        # Add limited chat history (last 2-3 turns to avoid context overflow)
        max_history = 2
        for turn in chat_history[-max_history:]:
            prompt_parts.append(f"<|im_start|>user\n{turn['user']}<|im_end|>")
            prompt_parts.append(f"<|im_start|>assistant\n{turn['assistant']}<|im_end|>")
        
        # Current query
        prompt_parts.append(f"<|im_start|>user\n{query}<|im_end|>")
        prompt_parts.append("<|im_start|>assistant\n")
        
        return "\n".join(prompt_parts)
    
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
