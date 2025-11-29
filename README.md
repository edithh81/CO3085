# 🍜 Food Order Chatbot with LLM/RAG

An online food ordering chatbot using LLM and RAG (Retrieval-Augmented Generation).

## 🎯 Features

- ✅ Intent recognition: order food, cancel order, query information
- ✅ RAG with FAISS vector database
- ✅ LLM (VinaLlama-2.7B 4-bit quantized) for natural responses
- ✅ Shopping cart and order management
- ✅ Web interface with Gradio

## 💻 System Requirements

- GPU: RTX 3050 (4GB VRAM) or better
- RAM: 16GB
- CUDA: < 13.0
- Python: 3.10+

## 🚀 Installation & Running

### Option 1: Run Locally

```bash
# Clone repository
git clone https://github.com/yourusername/rag-application.git
cd rag-application

# Install dependencies
pip install -r requirements.txt

# Generate menu data
python generate_menu.py

# Run chatbot
python app.py
```

Access: http://localhost:7860

### Option 2: Run with Docker

```bash
# Build image
docker build -t food-chatbot .

# Run container with GPU
docker run --gpus all -p 7860:7860 food-chatbot
```

Access: http://localhost:7860

### Option 3: Run on Google Colab (Recommended for Free GPU)

Use Google Colab's free GPU (Tesla T4 with 15GB VRAM) to run the chatbot:

1. **Open the Colab Notebook:**
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/rag-application/blob/main/colab_demo.ipynb)

2. **Or manually set up:**

```python
# In Google Colab notebook
!git clone https://github.com/yourusername/rag-application.git
%cd rag-application

# Install dependencies
!pip install -r requirements.txt

# Generate menu
!python generate_menu.py

# Run with public URL
!python app.py
```

3. **Enable GPU:** Go to `Runtime` → `Change runtime type` → Select `GPU` (T4)

4. **Access:** Gradio will provide a public URL (e.g., `https://xxxxx.gradio.live`)

**Colab Advantages:**
- ✅ Free Tesla T4 GPU (15GB VRAM)
- ✅ No local installation needed
- ✅ Pre-installed CUDA and PyTorch
- ✅ Public shareable URL
- ⚠️ Session timeout after 12 hours

## 📝 Usage

1. Open browser at `http://localhost:7860` (or Colab public URL)
2. Try these commands:
   - "Show me the menu"
   - "I want to order phở bò"
   - "How much is bún chả?"
   - "Add 2 iced coffee"
   - "View cart"
   - "Confirm order"

## 🏗️ Architecture

