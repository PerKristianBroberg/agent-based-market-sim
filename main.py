import random
from agents.buyer import Buyer
from agents.seller import Seller
from agents.strategies.basic import BasicStrategy
from agents.strategies.random_strategy import RandomStrategy
from agents.strategies.conservative import ConservativeStrategy
from agents.strategies.aggressive import AggressiveStrategy
from agents.strategies.learning import LearningStrategy
from market.market import Market
from simulation.simulation_runner import SimulationRunner
from analysis.metrics import Metrics
from analysis.plots import (
    plot_price_over_time,
    plot_trade_volume,
    plot_profit_by_strategy,
    plot_learning_convergence,
)

SEED = 42
NUM_ROUNDS = 1000
N_EACH = 5  # agents per strategy type

random.seed(SEED)


def make_buyers(n: int) -> list[Buyer]:
    buyers = []
    i = 0
    strategies = [
        ("basic",        lambda: BasicStrategy()),
        ("random",       lambda: RandomStrategy(noise=0.10)),
        ("conservative", lambda: ConservativeStrategy(margin=-0.15)),
        ("aggressive",   lambda: AggressiveStrategy(margin=+0.10)),
        ("learning",     lambda: LearningStrategy(direction=-1, step=0.05)),
    ]
    for _, factory in strategies:
        for _ in range(n):
            price = random.uniform(50, 150)
            buyers.append(Buyer(i, price, factory()))
            i += 1
    return buyers


def make_sellers(n: int, id_offset: int) -> list[Seller]:
    sellers = []
    i = id_offset
    strategies = [
        ("basic",        lambda: BasicStrategy()),
        ("random",       lambda: RandomStrategy(noise=0.10)),
        ("conservative", lambda: ConservativeStrategy(margin=+0.15)),
        ("aggressive",   lambda: AggressiveStrategy(margin=-0.10)),
        ("learning",     lambda: LearningStrategy(direction=+1, step=0.05)),
    ]
    for _, factory in strategies:
        for _ in range(n):
            price = random.uniform(50, 150)
            sellers.append(Seller(i, price, factory()))
            i += 1
    return sellers


buyers = make_buyers(N_EACH)
sellers = make_sellers(N_EACH, id_offset=len(buyers))

market = Market(buyers=buyers, sellers=sellers)
runner = SimulationRunner(market=market, num_rounds=NUM_ROUNDS)
runner.run()

all_agents = buyers + sellers
metrics = Metrics(trades=market.trade_history, agents=all_agents)
metrics.print_summary(num_rounds=NUM_ROUNDS)

print("\nGenerating plots...")
plot_price_over_time(market.trade_history)
plot_trade_volume(market.trade_history, num_rounds=NUM_ROUNDS)
plot_profit_by_strategy(all_agents)
plot_learning_convergence(all_agents)
print("Done. See plots/ folder.")
