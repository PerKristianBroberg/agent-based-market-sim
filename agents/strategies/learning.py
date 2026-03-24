from agents.strategies.strategy import Strategy


class LearningStrategy(Strategy):
    """
    Adapts the offer price based on trade outcomes.

    direction = -1 for buyers  (want to pay less)
    direction = +1 for sellers (want to receive more)

    After a successful trade:
      - Buyer lowers bid  (got a deal, try for cheaper next time)
      - Seller raises ask (sold, try for more next time)

    After a failed trade:
      - Buyer raises bid  (missed a deal, be more willing next time)
      - Seller lowers ask (missed a sale, be more flexible next time)

    The offset is clamped to [-max_offset, +max_offset] to prevent
    the agent drifting so far it never trades.
    """

    def __init__(self, direction: int, step: float = 0.05, max_offset: float = 0.30):
        if direction not in (-1, +1):
            raise ValueError("direction must be -1 (buyer) or +1 (seller)")
        self.direction = direction
        self.step = step
        self.max_offset = max_offset
        self._offset = 0.0  # fraction of reservation_price
        self.offset_history: list[float] = []

    def get_offer(self, reservation_price: float) -> float:
        return reservation_price * (1 + self._offset)

    def update(self, traded: bool, reservation_price: float, **context) -> None:
        if traded:
            self._offset += self.direction * self.step
        else:
            self._offset -= self.direction * self.step

        self._offset = max(-self.max_offset, min(self.max_offset, self._offset))
        self.offset_history.append(self._offset)

    @property
    def name(self) -> str:
        return "learning"

    @property
    def current_offset(self) -> float:
        return self._offset
