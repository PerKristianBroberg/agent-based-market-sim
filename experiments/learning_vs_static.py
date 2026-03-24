"""
Experiment 1: Learning vs Static
---------------------------------
Two isolated markets with identical reservation prices.
Market A: all basic (static) agents.
Market B: all learning agents.

Question: do learning agents generate more profit and surplus?
"""

import random
import matplotlib.pyplot as plt
from agents.buyer import Buyer
from agents.seller import Seller
from agents.strategies.basic import BasicStrategy
from agents.strategies.learning import LearningStrategy
from market.market import Market
from simulation.simulation_runner import SimulationRunner


NUM_AGENTS = 20
NUM_ROUNDS = 1000
SEED = 42


def _build_markets(reservation_prices_buyers, reservation_prices_sellers, strategy_type: str):
    if strategy_type == "static":
        buyers = [Buyer(i, p, BasicStrategy()) for i, p in enumerate(reservation_prices_buyers)]
        sellers = [Seller(i, p, BasicStrategy()) for i, p in enumerate(reservation_prices_sellers)]
    else:
        buyers = [Buyer(i, p, LearningStrategy(direction=-1)) for i, p in enumerate(reservation_prices_buyers)]
        sellers = [Seller(i, p, LearningStrategy(direction=+1)) for i, p in enumerate(reservation_prices_sellers)]
    return Market(buyers, sellers)


def run() -> None:
    random.seed(SEED)
    buyer_prices = [random.uniform(50, 150) for _ in range(NUM_AGENTS)]
    seller_prices = [random.uniform(50, 150) for _ in range(NUM_AGENTS)]

    market_static = _build_markets(buyer_prices, seller_prices, "static")
    market_learning = _build_markets(buyer_prices, seller_prices, "learning")

    SimulationRunner(market_static, NUM_ROUNDS).run()
    SimulationRunner(market_learning, NUM_ROUNDS).run()

    # --- metrics ---
    def rolling_avg(trades, window=30):
        if not trades:
            return [], []
        xs = [t.round_number for t in trades]
        ys = [t.price for t in trades]
        import pandas as pd
        s = pd.Series(ys, index=xs).sort_index()
        r = s.rolling(window, min_periods=1).mean()
        return r.index.tolist(), r.values.tolist()

    sx, sy = rolling_avg(market_static.trade_history)
    lx, ly = rolling_avg(market_learning.trade_history)

    static_agents = market_static.buyers + market_static.sellers
    learn_agents = market_learning.buyers + market_learning.sellers

    static_avg_profit = sum(a.total_profit for a in static_agents) / len(static_agents)
    learn_avg_profit = sum(a.total_profit for a in learn_agents) / len(learn_agents)
    static_trades = len(market_static.trade_history)
    learn_trades = len(market_learning.trade_history)

    print("\n=== Experiment 1: Learning vs Static ===")
    print(f"  {'':20s} {'Static':>10} {'Learning':>10}")
    print(f"  {'Trades':20s} {static_trades:>10} {learn_trades:>10}")
    print(f"  {'Trade rate':20s} {static_trades/NUM_ROUNDS*100:>9.1f}% {learn_trades/NUM_ROUNDS*100:>9.1f}%")
    print(f"  {'Avg profit/agent':20s} {static_avg_profit:>10.2f} {learn_avg_profit:>10.2f}")

    # --- plot ---
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Experiment 1: Learning vs Static Agents", fontsize=14, fontweight="bold")

    # Price over time
    ax = axes[0]
    ax.plot(sx, sy, color="#4C72B0", linewidth=2, label="Static (basic)")
    ax.plot(lx, ly, color="#9467BD", linewidth=2, label="Learning")
    ax.set_title("Rolling Average Trade Price")
    ax.set_xlabel("Round")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Profit comparison
    ax = axes[1]
    categories = ["Static", "Learning"]
    values = [static_avg_profit, learn_avg_profit]
    colors = ["#4C72B0", "#9467BD"]
    bars = ax.bar(categories, values, color=colors, alpha=0.85, width=0.4)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                f"{val:.1f}", ha="center", va="bottom", fontweight="bold")
    ax.set_title("Average Profit per Agent")
    ax.set_ylabel("Profit")
    ax.grid(True, alpha=0.3, axis="y")

    path = "plots/exp1_learning_vs_static.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")
