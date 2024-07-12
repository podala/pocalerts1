import faiss
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSearch:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.nlp_pipeline = pipeline('feature-extraction', model=self.model, tokenizer=self.tokenizer)
        self.index = None

    def create_embeddings(self, texts):
        embeddings = np.array([np.mean(self.nlp_pipeline(text)[0], axis=0) for text in texts])
        return embeddings

    def build_index(self, embeddings):
        d = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(d)
        self.index.add(embeddings)

    def search(self, query, k=5):
        query_embedding = np.mean(self.nlp_pipeline(query)[0], axis=0).reshape(1, -1)
        D, I = self.index.search(query_embedding, k)
        return I, D

def get_search_results(indices, distances, notes):
    results = []
    for i, dist in zip(indices[0], distances[0]):
        results.append({"note": notes[i], "distance": dist})
    return results
