from collections import defaultdict
from market.trade import Trade
from agents.agent import Agent


class Metrics:
    def __init__(self, trades: list[Trade], agents: list[Agent]):
        self.trades = trades
        self.agents = agents

    def total_trades(self) -> int:
        return len(self.trades)

    def average_price(self) -> float:
        if not self.trades:
            return 0.0
        return sum(t.price for t in self.trades) / len(self.trades)

    def total_surplus(self) -> float:
        return sum(t.total_surplus for t in self.trades)

    def by_strategy(self) -> dict:
        """Aggregate profit and trade count grouped by strategy name."""
        stats = defaultdict(lambda: {"profit": 0.0, "trades": 0, "agents": 0})
        for agent in self.agents:
            s = agent.strategy.name
            stats[s]["profit"] += agent.total_profit
            stats[s]["trades"] += agent.trades_completed
            stats[s]["agents"] += 1
        return dict(stats)

    def print_summary(self, num_rounds: int) -> None:
        print("=" * 44)
        print("SIMULATION RESULTS")
        print("=" * 44)
        print(f"Rounds run:       {num_rounds}")
        print(f"Trades completed: {self.total_trades()}")
        print(f"Trade rate:       {self.total_trades() / num_rounds * 100:.1f}%")
        print(f"Average price:    {self.average_price():.2f}")
        print(f"Total surplus:    {self.total_surplus():.2f}")

        print()
        print("Results by strategy:")
        print(f"  {'Strategy':<14} {'Agents':>6} {'Trades':>7} {'Total Profit':>13} {'Avg Profit':>11}")
        print(f"  {'-'*14} {'-'*6} {'-'*7} {'-'*13} {'-'*11}")
        for strategy, data in sorted(self.by_strategy().items()):
            avg = data["profit"] / data["agents"] if data["agents"] else 0
            print(f"  {strategy:<14} {data['agents']:>6} {data['trades']:>7} "
                  f"{data['profit']:>13.2f} {avg:>11.2f}")

        print()
        print("Top 5 agents by profit:")
        ranked = sorted(self.agents, key=lambda a: a.total_profit, reverse=True)[:5]
        for agent in ranked:
            print(f"  {agent}  profit={agent.total_profit:.2f}  trades={agent.trades_completed}")
        print("=" * 44)
