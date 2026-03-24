from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from market.trade import Trade
from agents.agent import Agent
from agents.strategies.learning import LearningStrategy


STRATEGY_COLORS = {
    "basic":        "#4C72B0",
    "random":       "#DD8452",
    "conservative": "#55A868",
    "aggressive":   "#C44E52",
    "learning":     "#9467BD",
}


def _save(fig: plt.Figure, path: str) -> None:
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def plot_price_over_time(trades: list[Trade], path: str = "plots/price_over_time.png") -> None:
    """Scatter of every trade price + 50-round rolling mean."""
    if not trades:
        return

    rounds = [t.round_number for t in trades]
    prices = [t.price for t in trades]

    series = pd.Series(prices, index=rounds).sort_index()
    rolling = series.rolling(window=50, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(rounds, prices, alpha=0.3, s=12, color="#4C72B0", label="Trade price")
    ax.plot(rolling.index, rolling.values, color="#C44E52", linewidth=2, label="50-round avg")

    ax.set_title("Trade Price Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Round")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _save(fig, path)


def plot_trade_volume(
    trades: list[Trade],
    num_rounds: int,
    window: int = 50,
    path: str = "plots/trade_volume.png",
) -> None:
    """Bar chart of trades per window of rounds."""
    bins = range(0, num_rounds + window, window)
    counts = defaultdict(int)
    for t in trades:
        bucket = (t.round_number // window) * window
        counts[bucket] += 1

    x = list(range(0, num_rounds, window))
    y = [counts[b] for b in x]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(x, y, width=window * 0.8, align="edge", color="#4C72B0", alpha=0.8)
    ax.set_title(f"Trade Volume per {window}-Round Window", fontsize=14, fontweight="bold")
    ax.set_xlabel("Round")
    ax.set_ylabel("Trades")
    ax.grid(True, alpha=0.3, axis="y")
    _save(fig, path)


def plot_profit_by_strategy(
    agents: list[Agent],
    path: str = "plots/profit_by_strategy.png",
) -> None:
    """Grouped bar: total profit and average profit per strategy."""
    stats = defaultdict(lambda: {"total": 0.0, "count": 0})
    for agent in agents:
        s = agent.strategy.name
        stats[s]["total"] += agent.total_profit
        stats[s]["count"] += 1

    strategies = sorted(stats.keys())
    totals = [stats[s]["total"] for s in strategies]
    averages = [stats[s]["total"] / stats[s]["count"] for s in strategies]
    colors = [STRATEGY_COLORS.get(s, "#888888") for s in strategies]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Profit by Strategy", fontsize=14, fontweight="bold")

    ax1.bar(strategies, totals, color=colors, alpha=0.85)
    ax1.set_title("Total Profit")
    ax1.set_ylabel("Profit")
    ax1.grid(True, alpha=0.3, axis="y")

    ax2.bar(strategies, averages, color=colors, alpha=0.85)
    ax2.set_title("Average Profit per Agent")
    ax2.set_ylabel("Profit")
    ax2.grid(True, alpha=0.3, axis="y")

    _save(fig, path)


def plot_learning_convergence(
    agents: list[Agent],
    path: str = "plots/learning_convergence.png",
) -> None:
    """
    For each learning agent, plot how their offer offset evolved over time.
    Shows buyers converging downward and sellers upward.
    """
    learning_agents = [a for a in agents if isinstance(a.strategy, LearningStrategy)]
    if not learning_agents:
        print("  No learning agents found, skipping convergence plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))

    for agent in learning_agents:
        history = agent.strategy.offset_history
        if not history:
            continue
        label = repr(agent)
        color = "#9467BD" if "Buyer" in label else "#C44E52"
        ax.plot(history, alpha=0.5, linewidth=1.2, color=color)

    # legend proxies
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color="#9467BD", label="Learning Buyers"),
        Line2D([0], [0], color="#C44E52", label="Learning Sellers"),
    ]
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.set_title("Learning Agent Offer Offset Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Times matched")
    ax.set_ylabel("Offer offset (fraction of reservation price)")
    ax.legend(handles=legend_elements)
    ax.grid(True, alpha=0.3)
    _save(fig, path)
