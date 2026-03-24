import random
from agents.buyer import Buyer
from agents.seller import Seller
from agents.strategies.basic import BasicStrategy
from agents.strategies.random_strategy import RandomStrategy
from agents.strategies.conservative import ConservativeStrategy
from agents.strategies.aggressive import AggressiveStrategy
from agents.strategies.learning import LearningStrategy
from agents.strategies.zip_strategy import ZIPStrategy
from agents.strategies.bandit_strategy import BanditStrategy
from market.market import Market
from simulation.simulation_runner import SimulationRunner
from analysis.metrics import Metrics
from analysis.plots import (
    plot_price_over_time,
    plot_trade_volume,
    plot_profit_by_strategy,
    plot_learning_convergence,
    plot_zip_margins,
    plot_bandit_arms,
)

SEED = 42
NUM_ROUNDS = 1000
N_EACH = 5  # agents per strategy type

random.seed(SEED)

BUYER_STRATEGIES = [
    lambda: BasicStrategy(),
    lambda: RandomStrategy(noise=0.10),
    lambda: ConservativeStrategy(margin=-0.15),
    lambda: AggressiveStrategy(margin=+0.10),
    lambda: LearningStrategy(direction=-1, step=0.05),
    lambda: ZIPStrategy(direction=-1),
    lambda: BanditStrategy(direction=-1),
]

SELLER_STRATEGIES = [
    lambda: BasicStrategy(),
    lambda: RandomStrategy(noise=0.10),
    lambda: ConservativeStrategy(margin=+0.15),
    lambda: AggressiveStrategy(margin=-0.10),
    lambda: LearningStrategy(direction=+1, step=0.05),
    lambda: ZIPStrategy(direction=+1),
    lambda: BanditStrategy(direction=+1),
]


def make_buyers(n: int) -> list[Buyer]:
    buyers, i = [], 0
    for factory in BUYER_STRATEGIES:
        for _ in range(n):
            buyers.append(Buyer(i, random.uniform(50, 150), factory()))
            i += 1
    return buyers


def make_sellers(n: int, id_offset: int) -> list[Seller]:
    sellers, i = [], id_offset
    for factory in SELLER_STRATEGIES:
        for _ in range(n):
            sellers.append(Seller(i, random.uniform(50, 150), factory()))
            i += 1
    return sellers


buyers = make_buyers(N_EACH)
sellers = make_sellers(N_EACH, id_offset=len(buyers))

market = Market(buyers=buyers, sellers=sellers)
SimulationRunner(market=market, num_rounds=NUM_ROUNDS).run()

all_agents = buyers + sellers
metrics = Metrics(trades=market.trade_history, agents=all_agents)
metrics.print_summary(num_rounds=NUM_ROUNDS)

print("\nGenerating plots...")
plot_price_over_time(market.trade_history)
plot_trade_volume(market.trade_history, num_rounds=NUM_ROUNDS)
plot_profit_by_strategy(all_agents)
plot_learning_convergence(all_agents)
plot_zip_margins(all_agents)
plot_bandit_arms(all_agents)
print("Done. See plots/ folder.")
