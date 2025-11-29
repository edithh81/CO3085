import json
import torch
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RAGSystem:
    def __init__(self, menu_path: str = "data/menu.json"):
        self.menu_path = menu_path
        self.menu_items = self.load_menu()
        
        # Use lightweight embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        self.index = None
        self.documents = []
        self.build_index()
    
    def load_menu(self) -> List[Dict]:
        """Load menu from JSON file"""
        with open(self.menu_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def build_index(self):
        """Build FAISS index from menu items"""
        print("Building FAISS index...")
        
        # Create documents for each menu item
        for item in self.menu_items:
            doc = f"{item['name']} - {item['category']}: {item['description']}. "
            doc += f"Giá: {item['price']:,}đ. "
            doc += f"Thành phần: {', '.join(item['ingredients'])}."
            self.documents.append({
                'text': doc,
                'item': item
            })
        
        # Generate embeddings
        texts = [doc['text'] for doc in self.documents]
        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
        print(f"Index built with {len(self.documents)} items")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant menu items"""
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
        
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx]['item'])
        
        return results
    
    def get_item_by_id(self, item_id: str) -> Dict:
        """Get menu item by ID"""
        for item in self.menu_items:
            if item['id'] == item_id:
                return item
        return None
    
    def get_item_by_name(self, name: str) -> Dict:
        """Get menu item by name (fuzzy match)"""
        name_lower = name.lower()
        for item in self.menu_items:
            if name_lower in item['name'].lower():
                return item
        return None
    
    def get_all_items(self) -> List[Dict]:
        """Get all available menu items"""
        return [item for item in self.menu_items if item['available']]
