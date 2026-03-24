from agents.agent import Agent
from agents.strategies.strategy import Strategy
from agents.strategies.basic import BasicStrategy


class Seller(Agent):
    """
    A seller with a minimum acceptable price (reservation_price).
    Actual ask is determined by the injected strategy.
    """

    def __init__(self, agent_id: int, reservation_price: float, strategy: Strategy = None):
        super().__init__(agent_id, reservation_price)
        self.strategy = strategy or BasicStrategy()

    def get_offer(self) -> float:
        return self.strategy.get_offer(self.reservation_price)

    def record_trade(self, price: float) -> None:
        self.total_profit += price - self.reservation_price
        self.trades_completed += 1

    def __repr__(self):
        return (f"Seller(id={self.agent_id}, reservation={self.reservation_price:.2f}, "
                f"strategy={self.strategy.name})")
