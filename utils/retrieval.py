import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(csv_path=r"data\sample_logs.csv"):
    df = pd.read_csv(csv_path)
    texts = df["message"].tolist()
    embeddings = model.encode(texts, normalize_embeddings=True)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(np.array(embeddings, dtype=np.float32))
    return index, df

def search_logs(query, index, df, top_k=3):
    query_emb = model.encode([query], normalize_embeddings=True)
    D, I = index.search(np.array(query_emb, dtype=np.float32), top_k)
    results = df.iloc[I[0]]
    return results, D[0]

if __name__ == "__main__":
    index, df = build_index()
    query = "packet loss in node 1"
    results, scores = search_logs(query, index, df)
    print(f"\nTop matches for query: {query}\n")
    for idx, row in enumerate(results.itertuples(index=False)):
        print(f"[{scores[idx]:.2f}] {row.timestamp} | {row.node_id} | {row.message}")
