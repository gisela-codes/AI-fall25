import pandas as pd
import numpy as np
from sklearn.metrics import ndcg_score
# from api_starter import query_ai
# from ranking_starter import precision_at_k

df = pd.read_csv("results.csv")

for qid, group in df.groupby("query_id"):
    y_true= group.sort_values("baseline_rank")["gold_label"].to_numpy()
    y_pred = group.sort_values("baseline_rank")["baseline_score"].to_numpy()
    baseline_ndcg = ndcg_score([y_true], [y_pred])

    y_pred_llm = group.sort_values("openai_score", ascending=False)["openai_score"].to_numpy()
    ndcg_llm = ndcg_score([y_true], [y_pred_llm])

    print(f"Query {qid}: baseline nDCG={baseline_ndcg:.3f}, LLM nDCG={ndcg_llm:.3f}")
