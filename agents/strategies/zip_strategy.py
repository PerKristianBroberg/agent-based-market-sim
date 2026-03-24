"""
Zero-Intelligence Plus (ZIP) strategy.

Reference:
    Cliff, D. & Bruten, J. (1997). Zero is not enough: On the lower limit
    of agent intelligence for continuous double auction markets.
    HP Laboratories Technical Report HPL-97-141.

How it works:
    Each agent maintains a profit margin `mu` (how far above/below their
    reservation price they quote). The margin is updated using a
    momentum-based rule toward a *target price* derived from the last
    observed market transaction.

    For sellers:
      - If the agent just traded OR its offer is below the last price
        → raise the margin (room to earn more)
      - Otherwise → lower the margin (need to become more competitive)

    For buyers the logic mirrors symmetrically.

    The update uses Widrow-Hoff (delta rule) with momentum:
        delta     = learning_rate * (target - current_offer)
        new_offer = current_offer + momentum * last_delta + delta

    This gives the agent inertia — it doesn't over-react to a single
    data point, but trends in outcomes do move its price steadily.
"""

import random
from agents.strategies.strategy import Strategy


class ZIPStrategy(Strategy):
    def __init__(
        self,
        direction: int,
        learning_rate: float = 0.10,
        momentum: float = 0.80,
        initial_margin: float = None,
    ):
        """
        direction: -1 for buyer (bids below reservation), +1 for seller (asks above)
        learning_rate: Widrow-Hoff step size (beta in the original paper)
        momentum:      weight on previous delta (gamma in the original paper)
        initial_margin: starting profit margin; randomised if None
        """
        if direction not in (-1, +1):
            raise ValueError("direction must be -1 (buyer) or +1 (seller)")
        self.direction = direction
        self.lr = learning_rate
        self.momentum = momentum
        self._mu = initial_margin if initial_margin is not None else random.uniform(0.05, 0.25)
        self._last_delta = 0.0
        self.mu_history: list[float] = []

    # --- offer -----------------------------------------------------------

    def get_offer(self, reservation_price: float) -> float:
        """Offer = reservation_price adjusted by profit margin in the agent's direction."""
        return reservation_price * (1 + self.direction * self._mu)

    # --- learning --------------------------------------------------------

    def update(self, traded: bool, reservation_price: float, **context) -> None:
        last_price = context.get("last_price")
        if last_price is None:
            return

        current_offer = self.get_offer(reservation_price)
        target = self._compute_target(traded, current_offer, last_price)
        if target is None:
            return

        # Widrow-Hoff delta rule with momentum
        delta = self.lr * (target - current_offer)
        new_offer = current_offer + self.momentum * self._last_delta + delta
        self._last_delta = delta

        # Back-calculate mu from the new offer
        raw_mu = self.direction * (new_offer / reservation_price - 1)
        self._mu = max(0.0, min(0.50, raw_mu))

        self.mu_history.append(self._mu)

    def _compute_target(self, traded: bool, current_offer: float, last_price: float):
        """
        Decide whether to raise or lower the offer and compute a target.
        Uses small random perturbations (R, A) as in the original paper.
        """
        R = random.uniform(0.0, 0.05)
        A = random.uniform(0.0, 0.05)

        if self.direction == +1:  # seller
            should_raise = traded or current_offer <= last_price
            return last_price * (1 + R) if should_raise else last_price * (1 - A)
        else:  # buyer
            should_lower = traded or current_offer >= last_price
            return last_price * (1 - R) if should_lower else last_price * (1 + A)

    @property
    def name(self) -> str:
        return "zip"
