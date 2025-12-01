# 🍜 Vietnamese Restaurant AI Chatbot

An intelligent Vietnamese restaurant chatbot using **VinaLLaMA-7B-Chat** with RAG for menu recommendations and order management with [DEMO](report/link_demo.txt).

## 🚀 Quick Start

**Two ways to run:**

### Option 1: Google Colab (Recommended) ⭐

1. Open `co3085.ipynb` in [Google Colab](https://colab.research.google.com/)
2. Enable GPU: `Runtime → Change runtime type → T4 GPU → Save`
3. Run all cells (Ctrl+F9)
4. Click the public Gradio link

### Option 2: Docker 🐳

```bash
# Run with Docker
docker build -t vietnamese-chatbot .
docker run -p 7860:7860 vietnamese-chatbot

# Or with Docker Compose
docker-compose up

# Access at: http://localhost:7860
```

---

## 📖 Features

✨ Natural Vietnamese conversations  
🍽️ Smart menu search with RAG  
🛒 Order management & tracking  
💬 Context-aware responses  

## 📁 Project Structure

```
CO3085/
├── app.py              # Gradio web interface
├── chatbot.py          # Chatbot logic
├── rag_system.py       # RAG with FAISS
├── data/
│   ├── menu.json       # 55 menu items
│   └── conversations.jsonl
├── Dockerfile          # Docker config
├── docker-compose.yml  # Docker Compose
└── co3085.ipynb       # Colab notebook
```

## 🐛 Troubleshooting

**Out of Memory:**
- Use 4-bit quantization (already enabled)
- Reduce `max_new_tokens` in `llm_handler.py`

**Port in use:**
- Change port: `demo.launch(server_port=7861)`

**Model download fails:**
- Check internet connection
- Use VPN if needed

## 📊 Performance

| Metric | Value |
|--------|-------|
| Model Size | 1.5GB (4-bit) |
| VRAM Usage | 3.5GB |
| Response Time | 2-5s |
| Accuracy | ~85% |

## 📝 License

MIT License

## 👥 Authors

- Edith - CO3085 NLP Project

---

**⭐ Star this repo if helpful!**

**Last Updated:** December 2024

