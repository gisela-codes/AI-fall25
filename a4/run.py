import argparse
from a4.ranking import rerank 
from a4.ranking import evaluate 

import pandas as pd
def main():
    parser = argparse.ArgumentParser(
        description=(
            "Run LLM-based ranking experiments.\n\n"
            "You can specify one or more models using --model.\n"
            "The script will compute relevance scores for query–candidate pairs "
            "using the selected language model(s)."
        ),
        formatter_class=argparse.RawTextHelpFormatter,  # allows newlines in description
    )

    parser.add_argument(
        "--model", "-m",
        nargs="+",
        default=["gpt-4.1", "gemini-2.5-flash-lite"],
        help=(
            "Model(s) to use for ranking.\n"
            "Examples:\n"
            "  -m gemini-1.5-pro gemini-2.0-flash-lite\n"
            "Supported families:\n"
            "  - GPT models: gpt-5-nano, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano\n"
            "  - Gemini models: gemini-2.5-flash, gemini-2.0-flash, gemini-2.0-flash-lite\n"
        )
    )
    parser.add_argument("--eval", action="store_true",
                        help="Evaluate results_all_models.csv (compute nDCG)")
    args = parser.parse_args()
    combined = None
    all_results = []
    KEYS=["query_id", "candidate_id"]
    df = pd.read_csv("rag_sample_queries_candidates.csv")
    # Ensure results are ordered by the baseline rank
    df.sort_values(["query_id", "baseline_rank"], inplace=True)
    q_ids = [10, 11, 12, 13]
    df = df[df["query_id"].isin(q_ids)] # ----uncomment this line out for testing-----
    if not args.eval:
        for model in args.model:
            print(f"trying {model}")
            df_model = rerank(model,df)
            score_col = f"{model}_score"
            rank_col  = f"{model}_rank"
            all_results.append(score_col)
            all_results.append(rank_col)
            if combined is None:
                combined = df_model[["query_id", "candidate_id", "baseline_rank", "baseline_score","gold_label"] + [score_col, rank_col]].copy()
            else:
                to_merge = df_model[KEYS + [score_col, rank_col]].copy()
                combined = combined.merge(to_merge, on=KEYS, how="left")

        combined.to_csv("results_all_models.csv", index=False)
    evaluate()

if __name__ == "__main__":
    main()