# Agent-Based Market Simulation

A from-scratch simulation of a double-auction market where autonomous agents trade goods, employ different pricing strategies, and adapt their behaviour based on outcomes.

Built to explore emergent market dynamics — how individual agent behaviour aggregates into market-level phenomena like price convergence and shock response.

---

## What it does

- **Agents** act as buyers or sellers, each with a private reservation price
- **Trade** occurs when a buyer's offer meets or exceeds a seller's ask; price is the midpoint
- **Strategies** determine how each agent sets its offer:

| Strategy | Description | Theory basis |
|---|---|---|
| `basic` | Offers exactly the reservation price | Baseline |
| `random` | Adds ±10% noise | Imperfect information |
| `conservative` | Holds back to maximise surplus per trade | — |
| `aggressive` | Moves toward the other side for more trades | — |
| `learning` | Adjusts offer ±step based on trade outcome | Feedback loop |
| `zip` | Momentum-based update toward last market price | Cliff & Bruten (1997) |
| `bandit` | Epsilon-greedy price arm selection, reward = profit | Sutton & Barto (2018) |

---

## Key findings

| Strategy | Avg Profit/Agent | Trade Rate |
|---|---|---|
| **zip** | **378.98** | 12.2% |
| basic | 301.43 | 17.0% |
| random | 293.07 | 17.6% |
| bandit | 291.18 | 19.2% |
| aggressive | 108.76 | 17.9% |
| conservative | 160.30 | 7.1% |
| learning | 160.09 | 14.0% |

**ZIP dominates** because it uses actual market transaction prices as a signal — it knows *what the market will bear*, not just whether it personally succeeded. This is the core insight from the Cliff & Bruten paper: market-level information is far more useful than individual-level feedback.

**Bandit lands mid-table** — it learns which price level yields the best expected profit, but starts cold (all Q-values = 0) and spends early rounds exploring. Given more rounds it would likely converge higher.

### Experiment results

**1. Learning vs Static (isolated markets)**
Learning agents generate 30% more trades and unlock surplus that static agents leave on the table.

**2. Demand shock (+40% buyer reservation prices at round 500)**
Both markets respond with higher prices, but learning agents absorb ~33% less price impact — their adaptive bids had already started converging before the shock.

**3. Price convergence (3000 rounds, learning agents)**
Price volatility (std dev) drops from **10.69** in the first 500 rounds to **3.98** in the last 500 — a 63% reduction. The market self-organises toward equilibrium.

---

## Project structure

```
capstone/
│
├── agents/
│   ├── agent.py                  # Abstract base class
│   ├── buyer.py
│   ├── seller.py
│   └── strategies/
│       ├── strategy.py           # Abstract strategy interface
│       ├── basic.py
│       ├── random_strategy.py
│       ├── conservative.py
│       ├── aggressive.py
│       ├── learning.py           # Feedback-loop adaptive strategy
│       ├── zip_strategy.py       # Zero-Intelligence Plus (Cliff & Bruten 1997)
│       └── bandit_strategy.py    # Epsilon-greedy bandit (Sutton & Barto 2018)
│
├── market/
│   ├── market.py                 # Matching engine
│   └── trade.py                  # Trade dataclass
│
├── simulation/
│   └── simulation_runner.py
│
├── analysis/
│   ├── metrics.py                # Summary statistics
│   └── plots.py                  # Matplotlib chart functions (6 plots)
│
├── experiments/
│   ├── learning_vs_static.py     # Experiment 1
│   ├── demand_shock.py           # Experiment 2
│   └── price_convergence.py      # Experiment 3
│
├── plots/                        # Generated charts (gitignored)
├── main.py                       # Run the main simulation
├── run_experiments.py            # Run all experiments
└── requirements.txt
```

---

## Setup

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows
# source .venv/bin/activate && pip install -r requirements.txt  # Mac/Linux
```

## Run

```bash
# Main simulation (1000 rounds, all 7 strategies, outputs plots/)
.venv/Scripts/python main.py

# All three experiments
.venv/Scripts/python run_experiments.py
```

---

## Design decisions

**Strategy pattern (composition over inheritance)**
Strategies are injected into agents at construction. Any strategy can be paired with any agent type, and new strategies require zero changes to existing code.

**Market context propagation**
The `Strategy.update()` method receives `**context` including the last transaction price. This enables market-aware strategies (ZIP) without coupling static strategies to unnecessary data.

**ZIP learning rule**
Uses the Widrow-Hoff delta rule with momentum:
```
delta     = learning_rate * (target_price - current_offer)
new_offer = current_offer + momentum * last_delta + delta
```
The target is derived from the last observed market transaction, with small random perturbations to prevent lock-in.

**Bandit reward signal**
Rather than using 0/1 (traded/not), the bandit uses actual profit as its reward. This prevents convergence to the most aggressive arm (which trades most but earns least) and instead finds the arm that maximises expected surplus.

---

## References

- Cliff, D. & Bruten, J. (1997). *Zero is not enough: On the lower limit of agent intelligence for continuous double auction markets.* HP Laboratories Technical Report HPL-97-141.
- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.), Chapter 2. MIT Press.

---

## Possible extensions

- Order book market instead of random matching
- Multi-good markets with substitutes
- UCB (Upper Confidence Bound) bandit variant
- Agent memory decay (older outcomes weighted less)
- Network effects (agents observe neighbours' trades)
