import os
from datetime import datetime

from chemotaxis import ChemotaxisSimulator

sim = ChemotaxisSimulator(num_steps=50, num_trajectories=10)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
trial_dir = os.path.join("results", f"trial_{timestamp}")
os.makedirs(trial_dir, exist_ok=True)

sim.plot_trajectories(save_path=os.path.join(trial_dir, "trajectories.png"))
sim.plot_concentration_vs_time(save_path=os.path.join(trial_dir, "concentration_vs_time.png"))
