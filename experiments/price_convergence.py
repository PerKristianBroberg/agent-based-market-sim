"""
Experiment 3: Price Convergence
---------------------------------
Run a long simulation (3000 rounds) with all-learning agents.
Show the rolling average price converging toward the theoretical
competitive equilibrium price.

Equilibrium price = the price where supply meets demand.
With uniform reservation prices on [50, 150] for both buyers and sellers,
the theoretical equilibrium is ~100 (the midpoint).

Question: do prices converge, and how long does it take?
"""

import random
import matplotlib.pyplot as plt
import pandas as pd
from agents.buyer import Buyer
from agents.seller import Seller
from agents.strategies.learning import LearningStrategy
from market.market import Market
from simulation.simulation_runner import SimulationRunner


NUM_AGENTS = 20
NUM_ROUNDS = 3000
SEED = 42
EQUILIBRIUM_PRICE = 100.0  # theoretical midpoint of [50, 150]


def run() -> None:
    random.seed(SEED)
    buyers = [Buyer(i, random.uniform(50, 150), LearningStrategy(direction=-1, step=0.03))
              for i in range(NUM_AGENTS)]
    sellers = [Seller(i, random.uniform(50, 150), LearningStrategy(direction=+1, step=0.03))
               for i in range(NUM_AGENTS)]

    market = Market(buyers, sellers)
    SimulationRunner(market, NUM_ROUNDS).run()

    trades = market.trade_history
    if not trades:
        print("No trades occurred.")
        return

    xs = [t.round_number for t in trades]
    ys = [t.price for t in trades]
    series = pd.Series(ys, index=xs).sort_index()
    rolling_50  = series.rolling(50,  min_periods=1).mean()
    rolling_200 = series.rolling(200, min_periods=1).mean()

    # measure convergence: std dev of prices in last 500 rounds
    late_prices = [t.price for t in trades if t.round_number > NUM_ROUNDS - 500]
    early_prices = [t.price for t in trades if t.round_number <= 500]
    early_std = pd.Series(early_prices).std() if early_prices else 0
    late_std  = pd.Series(late_prices).std()  if late_prices  else 0
    late_mean = pd.Series(late_prices).mean() if late_prices  else 0

    print("\n=== Experiment 3: Price Convergence ===")
    print(f"  Theoretical equilibrium price: {EQUILIBRIUM_PRICE:.2f}")
    print(f"  Observed late-run avg price:   {late_mean:.2f}")
    print(f"  Price std dev (rounds 1-500):  {early_std:.2f}")
    direction = "converging" if late_std < early_std else "not converging"
    print(f"  Price std dev (last 500):      {late_std:.2f}  ({direction})")

    # --- plot ---
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.scatter(xs, ys, alpha=0.2, s=8, color="#4C72B0", label="Trade price")
    ax.plot(rolling_50.index,  rolling_50.values,  color="#DD8452", linewidth=1.5, label="50-round avg")
    ax.plot(rolling_200.index, rolling_200.values, color="#C44E52", linewidth=2.5, label="200-round avg")
    ax.axhline(EQUILIBRIUM_PRICE, color="green", linewidth=1.5,
               linestyle="--", label=f"Theoretical equilibrium ({EQUILIBRIUM_PRICE})")

    ax.set_title("Experiment 3: Price Convergence (Learning Agents, 3000 Rounds)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Round")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True, alpha=0.3)

    path = "plots/exp3_price_convergence.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")
