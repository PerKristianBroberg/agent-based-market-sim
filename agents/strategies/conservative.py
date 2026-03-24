from agents.strategies.strategy import Strategy


class ConservativeStrategy(Strategy):
    """
    Holds back from the reservation price to maximize surplus.

    For buyers:  pass a negative margin (e.g. -0.15) → bids below max WTP
    For sellers: pass a positive margin (e.g. +0.15) → asks above min price

    This means fewer trades but higher profit per trade when they do occur.
    """

    def __init__(self, margin: float):
        if margin == 0:
            raise ValueError("margin must be non-zero for ConservativeStrategy")
        self.margin = margin

    def get_offer(self, reservation_price: float) -> float:
        return reservation_price * (1 + self.margin)

    @property
    def name(self) -> str:
        return "conservative"
