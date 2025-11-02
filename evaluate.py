import time
import numpy as np
import pandas as pd
from utils.retrieval import model, build_index, search_logs

def precision_at_k(query, relevant_keywords, index, df, k=3):
    start = time.time()
    results, _ = search_logs(query, index, df, top_k=k)
    latency = time.time() - start

    retrieved_texts = " ".join(results["message"].tolist()).lower()
    hits = sum(1 for kw in relevant_keywords if kw.lower() in retrieved_texts)
    precision = hits / len(relevant_keywords) if relevant_keywords else 0.0

    return {"query": query, "precision@k": round(precision, 2), "latency_s": round(latency, 3)}

def run_evaluation():
    index, df = build_index()

    test_queries = [
        {"query": "packet loss in node 1", "keywords": ["packet loss", "node_1"]},
        {"query": "cpu usage high", "keywords": ["cpu usage", "threshold"]},
        {"query": "link down alert", "keywords": ["link down", "interface"]},
        {"query": "power issue node 5", "keywords": ["power", "node_5"]},
    ]

    results = []
    for tq in test_queries:
        metrics = precision_at_k(tq["query"], tq["keywords"], index, df)
        results.append(metrics)
        print(f"[Eval] {tq['query']:<25} → P@3={metrics['precision@k']} | latency={metrics['latency_s']}s")

    df_results = pd.DataFrame(results)
    df_results.to_csv("data/eval_results.csv", index=False)
    print("\n[Eval] Results saved to data/eval_results.csv")

if __name__ == "__main__":
    run_evaluation()
