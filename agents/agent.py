from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, agent_id: int, reservation_price: float):
        self.agent_id = agent_id
        self.reservation_price = reservation_price
        self.trades_completed = 0
        self.total_profit = 0.0

    @abstractmethod
    def get_offer(self) -> float:
        """Return the price this agent is willing to trade at."""
        pass

    @abstractmethod
    def record_trade(self, price: float) -> None:
        """Update agent state after a trade."""
        pass

    def on_round_end(self, traded: bool) -> None:
        """Notify strategy of this round's outcome so it can adapt."""
        if hasattr(self, "strategy") and self.strategy is not None:
            self.strategy.update(traded, self.reservation_price)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.agent_id}, reservation={self.reservation_price:.2f})"
