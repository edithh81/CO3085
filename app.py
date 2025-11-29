import gradio as gr
from chatbot import FoodOrderChatbot
import uuid

# Initialize chatbot
print("Initializing chatbot...")
bot = FoodOrderChatbot()
print("Chatbot ready!")

# Get default welcome message (no LLM generation on startup)
welcome_msg = bot.llm._default_welcome()

def chat_interface(message, history, session_state):
    """Gradio chat interface"""
    if session_state is None:
        session_state = str(uuid.uuid4())
    
    response, session_id = bot.chat(message, session_state)
    
    return response, session_state

# Create Gradio interface
with gr.Blocks(title="Food Order Chatbot", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🍜 Chatbot Đặt Món Ăn Online
    
    Sử dụng LLM: **VinaLlama-2.7B-Chat** với RAG
    """)
    
    session_state = gr.State(None)
    
    chatbot = gr.Chatbot(
        value=[[None, welcome_msg]],  # Show default welcome message
        height=500,
        show_label=False
    )
    
    msg = gr.Textbox(
        label="Tin nhắn của bạn",
        placeholder="Ví dụ: Tôi muốn đặt phở bò và cà phê sữa đá...",
        show_label=False
    )
    
    with gr.Row():
        clear = gr.Button("🗑️ Xóa lịch sử chat")
        submit = gr.Button("📤 Gửi", variant="primary")
    
    def respond(message, chat_history, session):
        if session is None:
            session = str(uuid.uuid4())
        
        response, session = bot.chat(message, session)
        chat_history.append((message, response))
        return "", chat_history, session
    
    def clear_chat():
        """Clear chat and show welcome message again"""
        return [[None, welcome_msg]], str(uuid.uuid4())
    
    msg.submit(respond, [msg, chatbot, session_state], [msg, chatbot, session_state])
    submit.click(respond, [msg, chatbot, session_state], [msg, chatbot, session_state])
    clear.click(clear_chat, None, [chatbot, session_state])
    
    gr.Examples(
        examples=[
            "Cho tôi xem menu",
            "Tôi muốn đặt phở bò",
            "Có món nào có nước không?",
            "Giá bún chả bao nhiêu?",
            "Thêm 2 ly cà phê sữa đá",
            "Xem giỏ hàng",
            "Xác nhận đơn hàng"
        ],
        inputs=msg,
        label="💡 Câu hỏi gợi ý"
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
