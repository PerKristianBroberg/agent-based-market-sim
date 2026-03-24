"""
Epsilon-Greedy Multi-Armed Bandit strategy.

Reference:
    Sutton, R. S. & Barto, A. G. (2018). Reinforcement Learning:
    An Introduction (2nd ed.), Chapter 2: Multi-armed Bandits.
    MIT Press.

How it works:
    The agent discretises its possible offer prices into N evenly-spaced
    "arms" spanning ±spread around its reservation price.
    Each arm has an estimated Q-value — the average profit earned when
    that arm was chosen.

    Each round the agent either:
      - Exploits: picks the arm with the highest Q-value (prob 1 - epsilon)
      - Explores: picks a random arm                     (prob epsilon)

    After the outcome is observed the Q-value is updated via incremental
    sample-mean (the standard unbiased estimator):
        Q(a) ← Q(a) + 1/N(a) * (reward - Q(a))

    Reward = actual profit if a trade occurred, 0 otherwise.

    Because profit is used as the reward signal (not just 0/1), the bandit
    naturally learns to balance trade frequency against surplus per trade —
    it won't simply converge on the most aggressive (trade-maximising) arm.
"""

import random
from agents.strategies.strategy import Strategy


class BanditStrategy(Strategy):
    def __init__(
        self,
        direction: int,
        n_arms: int = 11,
        epsilon: float = 0.15,
        spread: float = 0.30,
    ):
        """
        direction: -1 for buyer, +1 for seller (used to compute profit)
        n_arms:    number of discrete price levels to choose from
        epsilon:   exploration probability
        spread:    total price range as a fraction of reservation price
                   (e.g. 0.30 → arms span from -15% to +15% of reservation)
        """
        if direction not in (-1, +1):
            raise ValueError("direction must be -1 (buyer) or +1 (seller)")
        self.direction = direction
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.spread = spread

        self._q: list[float] = [0.0] * n_arms   # estimated value per arm
        self._n: list[int]   = [0]   * n_arms   # pull count per arm
        self._current_arm: int = n_arms // 2    # start at the neutral mid-point
        self.arm_history: list[int] = []

    # --- offer -----------------------------------------------------------

    def get_offer(self, reservation_price: float) -> float:
        return self._arm_price(self._current_arm, reservation_price)

    def _arm_price(self, arm: int, reservation_price: float) -> float:
        """Map arm index linearly to a price in [res*(1-spread/2), res*(1+spread/2)]."""
        if self.n_arms == 1:
            return reservation_price
        step = self.spread / (self.n_arms - 1)
        offset = -self.spread / 2 + arm * step
        return reservation_price * (1 + offset)

    # --- learning --------------------------------------------------------

    def update(self, traded: bool, reservation_price: float, **context) -> None:
        arm = self._current_arm

        # Compute reward: actual profit if traded, 0 otherwise
        if traded:
            trade_price = context.get("trade_price", reservation_price)
            if self.direction == -1:   # buyer: profit = reservation - price paid
                reward = reservation_price - trade_price
            else:                      # seller: profit = price received - reservation
                reward = trade_price - reservation_price
            reward = max(0.0, reward)  # clip negatives (shouldn't happen, but safeguard)
        else:
            reward = 0.0

        # Incremental sample-mean update
        self._n[arm] += 1
        self._q[arm] += (reward - self._q[arm]) / self._n[arm]

        # Epsilon-greedy arm selection for next round
        if random.random() < self.epsilon:
            self._current_arm = random.randrange(self.n_arms)
        else:
            self._current_arm = max(range(self.n_arms), key=lambda i: self._q[i])

        self.arm_history.append(self._current_arm)

    @property
    def name(self) -> str:
        return "bandit"
