"""
Run all experiments and save plots to plots/.
"""
from experiments import learning_vs_static, demand_shock, price_convergence

print("Running experiments...")
learning_vs_static.run()
demand_shock.run()
price_convergence.run()
print("\nAll experiments complete. See plots/ folder.")
