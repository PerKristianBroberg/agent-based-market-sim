from abc import ABC, abstractmethod


class Strategy(ABC):
    """
    Determines how an agent sets its offer price relative to its reservation price.
    Decoupled from the agent so strategies can be swapped or extended easily.
    """

    @abstractmethod
    def get_offer(self, reservation_price: float) -> float:
        pass

    def update(self, traded: bool, reservation_price: float, **context) -> None:
        """
        Called after each round this agent was matched.
        context may include:
          trade_price   — actual transaction price (if traded)
          last_price    — most recent market trade price (always)
        Override in learning strategies.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass
