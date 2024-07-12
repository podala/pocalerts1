import faiss
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModel
import logging

class SemanticSearch:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.nlp_pipeline = pipeline('feature-extraction', model=self.model, tokenizer=self.tokenizer)
        self.index = None

    def create_embeddings(self, texts):
        return np.array([np.mean(self.nlp_pipeline(text)[0], axis=0) for text in texts])

    def build_index(self, embedding_dim):
        self.index = faiss.IndexFlatL2(embedding_dim)

    def add_to_index(self, embeddings):
        self.index.add(embeddings)

    def save_index(self, save_path):
        faiss.write_index(self.index, save_path)

    def load_index(self, load_path):
        self.index = faiss.read_index(load_path)

    def search(self, query, k=5):
        query_embedding = np.mean(self.nlp_pipeline(query)[0], axis=0).reshape(1, -1)
        D, I = self.index.search(query_embedding, k)
        return I, D

def get_search_results(indices, distances, notes):
    return [{"note": notes[i], "distance": dist} for i, dist in zip(indices[0], distances[0])]
