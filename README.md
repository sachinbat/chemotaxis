# E. coli Chemotaxis Simulation

Simulates the chemotactic behaviour of *E. coli* bacteria in a 2D grid. Each bacterium senses the concentration of a nutrient (food source at the origin) and moves toward it using a run-and-tumble strategy:

- **Run** — continue moving in the current direction when concentration is increasing (toward food).
- **Tumble** — pick a new random direction when concentration is decreasing (away from food).

Concentration is defined as the negative Euclidean distance from the origin. Higher (less negative) values indicate proximity to the food source.

## Installation

Requires Python 3 and matplotlib:

```bash
python3 -m pip install matplotlib
```

## Generating Plots

Run the main script:

```bash
python3 main.py
```

This generates two plots and saves them in a timestamped trial folder under `results/`:

- `trajectories.png` — 2D spatial paths of all simulated bacteria, with an optional average trajectory (dashed black line).
- `concentration_vs_time.png` — concentration over time for each trajectory, with an optional average (dashed black line).

Each run creates a new folder, e.g. `results/trial_20260405_133520/`, so previous results are never overwritten.

## Configuration

Adjust parameters in `main.py` or pass them to the `ChemotaxisSimulator` constructor:

| Parameter          | Default | Description                                      |
| ------------------ | ------- | ------------------------------------------------ |
| `num_steps`        | 50      | Number of time-steps per trajectory              |
| `num_trajectories` | 10      | Number of trajectories to generate               |
| `step_size`        | 1.0     | Distance travelled in a single step              |
| `bounds`           | (-10, 10) | Range for random starting positions on each axis |
