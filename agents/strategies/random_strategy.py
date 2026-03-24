import random
from agents.strategies.strategy import Strategy


class RandomStrategy(Strategy):
    """
    Adds uniform noise around the reservation price.
    Models an agent with imperfect knowledge of market conditions.
    """

    def __init__(self, noise: float = 0.10):
        self.noise = noise  # fraction of reservation price to vary by

    def get_offer(self, reservation_price: float) -> float:
        factor = random.uniform(1 - self.noise, 1 + self.noise)
        return reservation_price * factor

    @property
    def name(self) -> str:
        return "random"
