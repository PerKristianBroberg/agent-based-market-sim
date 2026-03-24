# Multi-Agent Market Simulation

A from-scratch simulation of a double-auction market where autonomous agents trade goods, employ different pricing strategies, and adapt their behaviour based on outcomes.

Built to explore emergent market dynamics — how individual agent behaviour aggregates into market-level phenomena like price convergence and shock response.

---

## What it does

- **Agents** act as buyers or sellers, each with a private reservation price
- **Trade** occurs when a buyer's offer meets or exceeds a seller's ask; price is the midpoint
- **Strategies** determine how each agent sets its offer:
  - `basic` — offers exactly the reservation price
  - `random` — adds noise (±10%) to simulate imperfect information
  - `conservative` — holds back to maximise surplus per trade
  - `aggressive` — moves toward the other side to maximise trade frequency
  - `learning` — adapts offer up or down based on whether the last trade succeeded
- **Experiments** test three specific questions about market behaviour

---

## Key findings

| Strategy | Avg Profit/Agent | Trade Rate |
|---|---|---|
| learning | **414.65** | 20.8% |
| basic | 290.63 | 17.9% |
| random | 191.26 | 12.6% |
| aggressive | 255.43 | 24.3% |
| conservative | 154.80 | 6.4% |

**Learning agents earn ~43% more profit** than basic agents despite not having any privileged information — they simply adjust their bids based on past outcomes.

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
│       └── learning.py           # Adaptive strategy
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
│   └── plots.py                  # Matplotlib chart functions
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
# Main simulation (1000 rounds, mixed strategies, outputs plots/)
.venv/Scripts/python main.py

# All experiments with individual plots
.venv/Scripts/python run_experiments.py
```

---

## Design decisions

**Strategy pattern (composition over inheritance)**
Strategies are injected into agents rather than subclassed. This means any strategy can be paired with any agent type, and new strategies can be added without touching existing code.

**Minimal learning rule**
The learning agent uses a single floating offset on its reservation price, adjusted ±5% per round based on trade outcome. No ML library required — the emergent behaviour comes purely from this simple feedback loop.

**Separation of concerns**
Agent logic (what to offer) is fully decoupled from market logic (how to match). The `Market` class only knows agents can produce offers and receive outcomes — it doesn't know anything about strategies.

---

## Possible extensions

- Order book market instead of random matching
- Multi-good markets with substitutes
- Agent memory decay (older outcomes weighted less)
- Network effects (agents observe neighbours' trades)
