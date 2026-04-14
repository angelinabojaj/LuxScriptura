# rag.py

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class RAGSystem:
    def __init__(self, json_path):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.docs = []
        self.refs = []

        for item in data:
            if item.get("text"):
                self.docs.append(item["text"])
                self.refs.append(item.get("paragraph", ""))

        self.embeddings = self.model.encode(self.docs).astype("float32")

        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def retrieve(self, query, k=5):
        q = self.model.encode([query]).astype("float32")
        _, idx = self.index.search(q, k)

        return [{"text": self.docs[i], "ref": self.refs[i]} for i in idx[0]]