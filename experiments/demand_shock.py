"""
Experiment 2: Demand Shock
---------------------------
Run 500 rounds normally, then increase every buyer's reservation price
by 40% (simulating a sudden surge in demand), then run 500 more rounds.

Question: how quickly does the market price respond?
          Do learning agents adapt faster than static agents?
"""

import random
import matplotlib.pyplot as plt
from agents.buyer import Buyer
from agents.seller import Seller
from agents.strategies.basic import BasicStrategy
from agents.strategies.learning import LearningStrategy
from market.market import Market


NUM_AGENTS = 20
ROUNDS_BEFORE = 500
ROUNDS_AFTER = 500
SHOCK_FACTOR = 1.40
SEED = 42


def _run_with_shock(buyer_prices, seller_prices, strategy_type: str):
    if strategy_type == "static":
        buyers = [Buyer(i, p, BasicStrategy()) for i, p in enumerate(buyer_prices)]
        sellers = [Seller(i, p, BasicStrategy()) for i, p in enumerate(seller_prices)]
    else:
        buyers = [Buyer(i, p, LearningStrategy(direction=-1)) for i, p in enumerate(buyer_prices)]
        sellers = [Seller(i, p, LearningStrategy(direction=+1)) for i, p in enumerate(seller_prices)]

    market = Market(buyers, sellers)

    # Phase 1: pre-shock
    for r in range(1, ROUNDS_BEFORE + 1):
        market.run_round(r)

    # Shock: increase buyer reservation prices
    for buyer in buyers:
        buyer.reservation_price *= SHOCK_FACTOR

    # Phase 2: post-shock
    for r in range(ROUNDS_BEFORE + 1, ROUNDS_BEFORE + ROUNDS_AFTER + 1):
        market.run_round(r)

    return market.trade_history


def _rolling(trades, window=30):
    if not trades:
        return [], []
    import pandas as pd
    xs = [t.round_number for t in trades]
    ys = [t.price for t in trades]
    s = pd.Series(ys, index=xs).sort_index()
    r = s.rolling(window, min_periods=1).mean()
    return r.index.tolist(), r.values.tolist()


def run() -> None:
    random.seed(SEED)
    buyer_prices = [random.uniform(50, 150) for _ in range(NUM_AGENTS)]
    seller_prices = [random.uniform(50, 150) for _ in range(NUM_AGENTS)]

    static_trades = _run_with_shock(buyer_prices, seller_prices, "static")
    learning_trades = _run_with_shock(buyer_prices, seller_prices, "learning")

    sx, sy = _rolling(static_trades)
    lx, ly = _rolling(learning_trades)

    # Price before vs after shock
    def avg_price(trades, after_round):
        subset = [t.price for t in trades if t.round_number > after_round]
        return sum(subset) / len(subset) if subset else 0

    static_before = sum(t.price for t in static_trades if t.round_number <= ROUNDS_BEFORE)
    static_before /= max(1, sum(1 for t in static_trades if t.round_number <= ROUNDS_BEFORE))
    static_after = avg_price(static_trades, ROUNDS_BEFORE)
    learn_before = sum(t.price for t in learning_trades if t.round_number <= ROUNDS_BEFORE)
    learn_before /= max(1, sum(1 for t in learning_trades if t.round_number <= ROUNDS_BEFORE))
    learn_after = avg_price(learning_trades, ROUNDS_BEFORE)

    print("\n=== Experiment 2: Demand Shock ===")
    print(f"  Shock at round {ROUNDS_BEFORE}: buyer reservation prices ×{SHOCK_FACTOR}")
    print(f"  {'':22s} {'Static':>10} {'Learning':>10}")
    print(f"  {'Avg price (pre-shock)':22s} {static_before:>10.2f} {learn_before:>10.2f}")
    print(f"  {'Avg price (post-shock)':22s} {static_after:>10.2f} {learn_after:>10.2f}")
    print(f"  {'Price increase':22s} {static_after - static_before:>+10.2f} {learn_after - learn_before:>+10.2f}")

    # --- plot ---
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(sx, sy, color="#4C72B0", linewidth=2, label="Static agents")
    ax.plot(lx, ly, color="#9467BD", linewidth=2, label="Learning agents")
    ax.axvline(x=ROUNDS_BEFORE, color="red", linewidth=1.5, linestyle="--", label=f"Demand shock (×{SHOCK_FACTOR})")
    ax.set_title("Experiment 2: Price Response to Demand Shock", fontsize=14, fontweight="bold")
    ax.set_xlabel("Round")
    ax.set_ylabel("Rolling Average Price")
    ax.legend()
    ax.grid(True, alpha=0.3)

    path = "plots/exp2_demand_shock.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")
