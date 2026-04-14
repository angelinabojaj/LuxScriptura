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

        # build docs + refs properly
        for item in data:
            if isinstance(item, dict):
                text = item.get("text")
                if text:
                    self.docs.append(text)
                    self.refs.append(item.get("ref", ""))
            elif isinstance(item, str):
                self.docs.append(item)
                self.refs.append("")

        if len(self.docs) == 0:
            raise ValueError("No valid documents found in JSON file.")

        # encode docs (NOT empty list)
        self.embeddings = self.model.encode(self.docs)

        self.embeddings = np.array(self.embeddings).astype("float32")

        # ensure 2D safety
        if self.embeddings.ndim == 1:
            self.embeddings = self.embeddings.reshape(1, -1)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def retrieve(self, query, k=5):
        q = self.model.encode([query]).astype("float32")

        _, idx = self.index.search(q, k)

        return [
            {"text": self.docs[i], "ref": self.refs[i]}
            for i in idx[0]
            if i < len(self.docs)
        ]