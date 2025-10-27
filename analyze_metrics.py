import os
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_metrics(persona):
    """Load metrics JSON for a persona into a pandas DataFrame."""
    path = os.path.join("models", persona, "training_metrics.json")
    if not os.path.exists(path):
        print(f"[WARN] No metrics found for {persona} persona.")
        return pd.DataFrame()
    with open(path, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["persona"] = persona
    return df

def plot_comparison(df1, df2, metric, ylabel, title):
    """Plot a comparison between two personas for a given metric."""
    plt.figure(figsize=(8,5))
    plt.plot(df1["episode"], df1[metric], label="Survival", color="blue")
    plt.plot(df2["episode"], df2[metric], label="Combat", color="red")
    plt.xlabel("Episode")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    os.makedirs("graphs", exist_ok=True)
    save_path = os.path.join("graphs", f"{metric}_comparison.png")
    plt.savefig(save_path)
    plt.close()
    print(f"[INFO] Saved graph: {save_path}")

def main():
    # Load both personas' metrics
    df_survival = load_metrics("survival")
    df_combat = load_metrics("combat")

    if df_survival.empty or df_combat.empty:
        print("[ERROR] Missing one or both persona metric files.")
        return

    # Ensure same episode range (optional)
    min_len = min(len(df_survival), len(df_combat))
    df_survival = df_survival.head(min_len)
    df_combat = df_combat.head(min_len)

    # Plot comparisons
    metrics_to_plot = [
        ("total_reward", "Total Reward", "Total Reward per Episode"),
        ("average_elixir", "Average Elixir", "Average Elixir per Episode"),
        ("troops_deployed", "Troops Deployed", "Troops Deployed per Episode"),
        ("merge_events", "Merge Events", "Merges per Episode"),
        ("time_alive", "Time Alive (s)", "Survival Time per Episode"),
    ]

    for metric, ylabel, title in metrics_to_plot:
        if metric in df_survival.columns and metric in df_combat.columns:
            plot_comparison(df_survival, df_combat, metric, ylabel, title)

if __name__ == "__main__":
    main()
