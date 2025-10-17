#!/usr/bin/env python3
"""
Evaluate retrieval quality on the RAG sample dataset.

Computes Precision@K, Recall@K, and nDCG@K
for each query and averages the results.

Assumes the dataset columns:
  query_id, query_text, candidate_id, candidate_text,
  baseline_rank, baseline_score, gold_label
"""
import time
import pandas as pd
import numpy as np
from sklearn.metrics import ndcg_score
import matplotlib.pyplot as plt
import seaborn as sns
from api import query_ai
from openai import RateLimitError

# ---------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------
def precision_at_k(labels, k):
    """labels: list/array of 0/1 relevance sorted by baseline rank"""
    topk = labels[:k]
    return np.sum(topk) / len(topk)

def recall_at_k(labels, k):
    """Recall = retrieved relevant / total relevant"""
    total_relevant = np.sum(labels)
    if total_relevant == 0:
        return np.nan  # undefined
    topk = labels[:k]
    return np.sum(topk) / total_relevant

def ndcg_at_k(labels, k):
    """Compute nDCG@k with binary relevance (0/1)."""
    labels = np.array(labels)
    k = min(k, len(labels))
    gains = (2 ** labels[:k] - 1)
    discounts = 1 / np.log2(np.arange(2, k + 2))
    dcg = np.sum(gains * discounts)

    # Ideal DCG: sorted by true relevance
    ideal = np.sort(labels)[::-1]
    ideal_gains = (2 ** ideal[:k] - 1)
    idcg = np.sum(ideal_gains * discounts)
    return 0.0 if idcg == 0 else dcg / idcg


def rerank(model):
    # ---------------------------------------------------------------------
    # 1. Load data
    # ---------------------------------------------------------------------
    df = pd.read_csv("rag_sample_queries_candidates.csv")

    # Ensure results are ordered by the baseline rank
    df.sort_values(["query_id", "baseline_rank"], inplace=True)
    # df = df.iloc[:13, :]
    # print(df)
    # ---------------------------------------------------------------------
    # 2. Query LLM and save scores
    # ---------------------------------------------------------------------
    scores = []
    for q_text, c_text in df[["query_text", "candidate_text"]].itertuples(index=False):
        for attempt in range(3):
            try:
                score = query_ai(model, q_text, c_text)
                scores.append(score)
                print(f"{model}: {score}")
                break 
            except RateLimitError:
                wait = 4 + (2 * attempt)
                print(f"Rate limited. Retrying in {wait}s...")
                time.sleep(wait)
            scores.append(None)
        time.sleep(1)

    df[f"{model}_score"] = scores

    # ---------------------------------------------------------------------
    # 3. Rerank and Save
    # ---------------------------------------------------------------------
    df[f"{model}_rank"] = (
        df.groupby("query_id")[f"{model}_score"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    df_sorted = (
        df.sort_values(
            ["query_id", f"{model}_rank", f"{model}_score"],
            ascending=[True, True, False]
        )
        .reset_index(drop=True)
    )
    
    results = df_sorted[
        [
            "query_id",
            "candidate_id",
            "baseline_rank",
            "baseline_score",
            "gold_label",
            f"{model}_score",
            f"{model}_rank",
        ]
    ]
    return results

def evaluate():
    df = pd.read_csv("results_all_models.csv")
    results=[]
    model_cols = [
        c for c in df.columns
        if c.endswith("_score") and not c.startswith("baseline")
    ]
    models = [c.replace("_score", "") for c in model_cols]
    for qid, group in df.groupby("query_id"):
        y_true= group.sort_values("baseline_rank")["gold_label"].to_numpy()
        y_pred = group.sort_values("baseline_rank")["baseline_score"].to_numpy()
        baseline_ndcg = ndcg_score([y_true], [y_pred])

        row = {"query_id": qid, "baseline_ndcg": baseline_ndcg}
        for model in models:
            y_pred_llm = group.sort_values(f"{model}_score", ascending=False)[f"{model}_score"].to_numpy()
            row[f"{model}_ndcg"] = ndcg_score([y_true], [y_pred_llm])
        results.append(row)
        # print(f"Query {qid}: baseline nDCG={baseline_ndcg:.3f}, LLM nDCG={ndcg_llm:.3f}")
        # Query 1: baseline nDCG=1.000, LLM nDCG=1.000
        # Query 2: baseline nDCG=0.967, LLM nDCG=0.958
    df_out = pd.DataFrame(results)
    print(df_out)
    
    plt.figure(figsize=(10,5))
    sns.set_palette("husl")
    
    for model in models:
        sns.lineplot(data=df_out, x="query_id", y=f"{model}_ndcg", marker="o", alpha=0.5, label=model)
    sns.lineplot(
        data=df_out,
        x="query_id",
        y="baseline_ndcg",
        color="black",
        linestyle="dotted",
        label="Baseline"
    )
    plt.title("nDCG per Query")
    plt.xlabel("Query ID")
    plt.ylabel("nDCG Score")
    plt.xticks(range(1, len(df_out) + 1))
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.show()
    # Print averages
    avg = df_out.mean(numeric_only=True)
    print("\nAverage nDCG per model:")
    print(avg)

    return df_out

# create a graph where x axis is my queries and graph 3 lines. the baseline nDCG and the two LLM nDCG 

    # results.to_csv("results.csv", index=False)
    # ---------------------------------------------------------------------
    # 3. Compute metrics per query
    # ---------------------------------------------------------------------
    # results = []
    # K = 3

    # for qid, group in df.groupby("query_id"):
    #     labels = group["gold_label"].tolist()
    #     p = precision_at_k(labels, K)
    #     r = recall_at_k(labels, K)
    #     n = ndcg_at_k(labels, K)
    #     results.append({"query_id": qid, f"precision@{K}": p, f"recall@{K}": r, f"nDCG@{K}": n})

    # metrics = pd.DataFrame(results)

    # # ---------------------------------------------------------------------
    # # 4. Display per-query and average metrics
    # # ---------------------------------------------------------------------
    # print(metrics.round(3))
    # print("\nAverage metrics:")
    # print(metrics[[f"precision@{K}", f"recall@{K}", f"nDCG@{K}"]].mean().round(3))

    # return df_sorted