"""
Vector Embedding and Semantic RAG Retrieval Engine for Embedded Failure Patterns
Zero external heavy dependencies; pure-Python TF-IDF and Cosine Similarity.
"""

import json
import math
import re
from typing import Dict, List, Tuple


class RAGEngine:
    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.patterns: List[Dict] = []
        self.vocab: Dict[str, int] = {}
        self.doc_vectors: List[List[float]] = []
        self._load_and_index()

    def _tokenize(self, text: str) -> List[str]:
        cleaned = re.sub(r"[^a-zA-Z0-9_\-]", " ", text.lower())
        tokens = [t for t in cleaned.split() if len(t) > 2]
        return tokens

    def _load_and_index(self):
        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.patterns = json.load(f)

        # Build vocabulary
        doc_tokens_list = []
        for p in self.patterns:
            doc_str = f"{p['subsystem']} {p['failure_type']} {p['root_cause']} " + " ".join(p['keywords'])
            tokens = self._tokenize(doc_str)
            doc_tokens_list.append(tokens)
            for t in tokens:
                if t not in self.vocab:
                    self.vocab[t] = len(self.vocab)

        # Build TF-IDF vectors
        num_docs = len(self.patterns)
        idf = {}
        for t in self.vocab:
            df = sum(1 for d in doc_tokens_list if t in d)
            idf[t] = math.log((num_docs + 1) / (df + 1)) + 1.0

        for tokens in doc_tokens_list:
            vec = [0.0] * len(self.vocab)
            tf = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            for t, count in tf.items():
                idx = self.vocab[t]
                vec[idx] = (count / len(tokens)) * idf[t]
            # Normalize vector
            norm = math.sqrt(sum(v * v for v in vec))
            if norm > 0:
                vec = [v / norm for v in vec]
            self.doc_vectors.append(vec)

    def query(self, text: str, top_k: int = 3) -> List[Tuple[Dict, float]]:
        tokens = self._tokenize(text)
        if not tokens:
            return []

        query_vec = [0.0] * len(self.vocab)
        for t in tokens:
            if t in self.vocab:
                query_vec[self.vocab[t]] += 1.0

        q_norm = math.sqrt(sum(v * v for v in query_vec))
        if q_norm == 0:
            return []
        query_vec = [v / q_norm for v in query_vec]

        scores = []
        for idx, doc_vec in enumerate(self.doc_vectors):
            dot = sum(q * d for q, d in zip(query_vec, doc_vec))
            scores.append((self.patterns[idx], dot))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
