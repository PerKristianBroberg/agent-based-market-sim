from agents.strategies.strategy import Strategy


class AggressiveStrategy(Strategy):
    """
    Moves toward the other side to maximise trade frequency.

    For buyers:  pass a positive margin (e.g. +0.10) → bids above reservation
                 (willing to overpay slightly to secure a deal)
    For sellers: pass a negative margin (e.g. -0.10) → asks below reservation
                 (willing to undersell slightly to secure a deal)

    More trades, but lower surplus per trade.
    """

    def __init__(self, margin: float):
        if margin == 0:
            raise ValueError("margin must be non-zero for AggressiveStrategy")
        self.margin = margin

    def get_offer(self, reservation_price: float) -> float:
        return reservation_price * (1 + self.margin)

    @property
    def name(self) -> str:
        return "aggressive"
