# E. coli Chemotaxis Simulation

Simulates the chemotactic behaviour of *E. coli* bacteria in a 2D grid. Each bacterium senses the concentration of a nutrient (food source at the origin) and moves toward it using a run-and-tumble strategy:

- **Run** — continue moving in the current direction when concentration is increasing (toward food).
- **Tumble** — pick a new random direction when concentration is decreasing (away from food).

Concentration is defined as the negative Euclidean distance from the origin. Higher (less negative) values indicate proximity to the food source.

## Installation

Requires Python 3, matplotlib, and Flask:

```bash
python3 -m pip install matplotlib flask
```

## Generating Plots Locally

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

## API

Start the development server:

```bash
flask run --port 5000
```

### `POST /simulate`

Run a simulation and return the resulting plots as base64-encoded PNG images.

**Request body** (JSON, all fields optional):

| Field               | Type   | Default    | Description                                       |
| ------------------- | ------ | ---------- | ------------------------------------------------- |
| `num_steps`         | int    | 50         | Number of time-steps per trajectory               |
| `num_trajectories`  | int    | 10         | Number of trajectories to generate                |
| `step_size`         | float  | 1.0        | Distance travelled in a single step               |
| `bounds`            | list   | [-10, 10]  | `[min, max]` range for random starting positions  |

**Example request:**

```bash
curl -X POST http://127.0.0.1:5000/simulate \
  -H "Content-Type: application/json" \
  -d '{"num_steps": 20, "num_trajectories": 5}'
```

**Response** (JSON):

```json
{
  "trajectories": "<base64-encoded PNG>",
  "concentration_vs_time": "<base64-encoded PNG>"
}
```

The `trajectories` field contains the 2D spatial plot and `concentration_vs_time` contains the concentration-over-time plot. Both are PNG images encoded as base64 strings, ready to embed in an `<img>` tag:

```html
<img src="data:image/png;base64,<base64-string>" />
```

Invalid input returns a `400` status with an error message in the `error` field.
