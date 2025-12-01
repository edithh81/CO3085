import re
import uuid
from typing import List, Dict, Tuple
from rag_system import RAGSystem
from llm_handler import LLMHandler
from database import Database

class FoodOrderChatbot:
    def __init__(self):
        self.rag = RAGSystem()
        self.llm = LLMHandler()
        self.db = Database()
        self.sessions = {}
    
    def get_session(self, session_id: str) -> Dict:
        """Get or create session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'cart': [],
                'chat_history': [],
                'current_order_id': None
            }
        return self.sessions[session_id]
    
    def parse_intent(self, query: str) -> str:
        """Parse user intent"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['đặt', 'gọi', 'order', 'thêm', 'cho tôi', 'muốn']):
            return 'order'
        elif any(word in query_lower for word in ['hủy', 'cancel', 'bỏ']):
            return 'cancel'
        elif any(word in query_lower for word in ['menu', 'món', 'có gì', 'thực đơn', 'xem menu']):
            return 'menu_info'
        elif any(word in query_lower for word in ['giá', 'bao nhiêu', 'price', 'tiền']):
            return 'price_info'
        elif any(word in query_lower for word in ['giỏ', 'cart', 'đơn hàng', 'xem giỏ']):
            return 'view_cart'
        elif any(word in query_lower for word in ['xác nhận', 'confirm']):
            return 'confirm_order'
        elif any(word in query_lower for word in ['nước', 'soup', 'canh', 'lỏng']):
            return 'soup_dishes'
        else:
            return 'general'
    
    def extract_items_from_query(self, query: str) -> List[str]:
        """Extract food items from query"""
        # Simple extraction - can be improved with NER
        items = []
        for item in self.rag.menu_items:
            if item['name'].lower() in query.lower():
                items.append(item['name'])
        return items
    
    def handle_order(self, query: str, session: Dict) -> str:
        """Handle order intent"""
        items = self.extract_items_from_query(query)
        
        if not items:
            # Use RAG to find similar items
            results = self.rag.search(query, top_k=3)
            response = "Tôi tìm thấy các món sau trong menu:\n\n"
            for item in results:
                response += f"• {item['name']} - {item['price']:,}đ\n  {item['description']}\n\n"
            response += "Bạn muốn đặt món nào ạ?"
            return response
        
        # Add items to cart
        for item_name in items:
            item = self.rag.get_item_by_name(item_name)
            if item:
                session['cart'].append(item)
        
        # Generate confirmation
        response = "Đã thêm vào giỏ hàng:\n\n"
        total = 0
        for item in session['cart']:
            response += f"• {item['name']} - {item['price']:,}đ\n"
            total += item['price']
        
        response += f"\nTổng cộng: {total:,}đ\n"
        response += "Bạn có muốn đặt thêm món nào không?"
        
        return response
    
    def handle_confirm_order(self, session: Dict, session_id: str) -> str:
        """Confirm and create order"""
        if not session['cart']:
            return "Giỏ hàng của bạn đang trống. Vui lòng chọn món trước khi xác nhận."
        
        total = sum(item['price'] for item in session['cart'])
        order_id = self.db.create_order(session_id, session['cart'], total)
        
        session['current_order_id'] = order_id
        session['cart'] = []
        
        return f"✓ Đơn hàng #{order_id} đã được tạo thành công!\nTổng tiền: {total:,}đ\nChúng tôi sẽ chuẩn bị món ăn ngay. Cảm ơn bạn!"
    
    def handle_cancel(self, query: str, session: Dict) -> str:
        """Handle cancel intent"""
        if session['current_order_id']:
            success = self.db.cancel_order(session['current_order_id'])
            if success:
                order_id = session['current_order_id']
                session['current_order_id'] = None
                return f"Đã hủy đơn hàng #{order_id}."
            else:
                return "Không thể hủy đơn hàng. Đơn hàng có thể đã được xử lý."
        else:
            return "Bạn chưa có đơn hàng nào để hủy."
    
    def handle_soup_dishes(self, query: str) -> str:
        """Handle request for soup/liquid dishes"""
        soup_items = []
        keywords = ['phở', 'bún', 'hủ tiếu', 'canh', 'lẩu', 'súp', 'miến', 'bánh canh']
        
        for item in self.rag.menu_items:
            if any(keyword in item['name'].lower() for keyword in keywords):
                soup_items.append(item)
        
        if not soup_items:
            return "Xin lỗi, hiện tại chúng tôi không có món nước nào."
        
        response = "🍜 Các món có nước trong menu:\n\n"
        for item in soup_items[:8]:  # Limit to 8 items
            response += f"• {item['name']:<25} {item['price']:>8,}đ\n  {item['description']}\n\n"
        
        response += "Bạn muốn đặt món nào ạ?"
        return response
    
    def handle_menu_info(self, query: str) -> str:
        """Handle menu information requests"""
        # Show by categories
        categories = {}
        for item in self.rag.menu_items:
            cat = item['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        response = "📋 THỰC ĐƠN NHÀ HÀNG\n\n"
        
        for category, items in list(categories.items())[:3]:  # Show 3 categories
            response += f"▸ {category.upper()}\n"
            for item in items[:5]:  # 5 items per category
                response += f"  • {item['name']:<22} {item['price']:>8,}đ\n"
            response += "\n"
        
        response += "Bạn muốn biết thêm về món nào hoặc muốn đặt món không ạ?"
        return response
    
    def chat(self, message: str, session_id: str = None) -> Tuple[str, str]:
        """Main chat function"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session = self.get_session(session_id)
        intent = self.parse_intent(message)
        
        # Handle specific intents without LLM (faster, more accurate)
        if intent == 'order':
            response = self.handle_order(message, session)
        elif intent == 'confirm_order':
            response = self.handle_confirm_order(session, session_id)
        elif intent == 'cancel':
            response = self.handle_cancel(message, session)
        elif intent == 'view_cart':
            if session['cart']:
                response = "🛒 Giỏ hàng của bạn:\n\n"
                total = 0
                for item in session['cart']:
                    response += f"• {item['name']:<25} {item['price']:>8,}đ\n"
                    total += item['price']
                response += f"\n💰 Tổng cộng: {total:,}đ\n\n"
                response += "Bạn muốn đặt thêm hoặc xác nhận đơn hàng không?"
            else:
                response = "Giỏ hàng của bạn đang trống. Hãy chọn món từ menu nhé!"
        elif intent == 'menu_info':
            response = self.handle_menu_info(message)
        elif intent == 'soup_dishes':
            response = self.handle_soup_dishes(message)
        else:
            # Use RAG + LLM for general queries (improved)
            relevant_items = self.rag.search(message, top_k=3)
            
            if relevant_items:
                context = "Các món phù hợp:\n"
                for item in relevant_items:
                    context += f"- {item['name']}: {item['description']} (Giá: {item['price']:,}đ)\n"
            else:
                context = ""
            
            prompt = self.llm.create_prompt(context, message, session['chat_history'])
            llm_response = self.llm.generate_response(prompt, max_length=150)
            
            # If LLM response is poor or empty, provide fallback
            if len(llm_response) < 10:
                if relevant_items:
                    response = f"Tôi tìm thấy các món sau:\n\n"
                    for item in relevant_items:
                        response += f"• {item['name']} - {item['price']:,}đ\n  {item['description']}\n\n"
                    response += "Bạn muốn đặt món nào ạ?"
                else:
                    response = "Xin lỗi, tôi chưa hiểu rõ yêu cầu của bạn. Bạn có thể hỏi về menu, đặt món, hoặc xem giỏ hàng nhé!"
            else:
                response = llm_response
        
        # Update chat history
        session['chat_history'].append({
            'user': message,
            'assistant': response
        })
        
        # Keep history manageable
        if len(session['chat_history']) > 10:
            session['chat_history'] = session['chat_history'][-10:]
        
        return response, session_id
