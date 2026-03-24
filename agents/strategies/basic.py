from agents.strategies.strategy import Strategy


class BasicStrategy(Strategy):
    """Offers exactly the reservation price. No adjustment."""

    def get_offer(self, reservation_price: float) -> float:
        return reservation_price

    @property
    def name(self) -> str:
        return "basic"
