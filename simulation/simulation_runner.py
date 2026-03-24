from market.market import Market
from market.trade import Trade


class SimulationRunner:
    def __init__(self, market: Market, num_rounds: int = 1000):
        self.market = market
        self.num_rounds = num_rounds

    def run(self) -> list[Trade]:
        for round_num in range(1, self.num_rounds + 1):
            self.market.run_round(round_num)
        return self.market.trade_history
