"""
Flask API for the E. coli chemotaxis simulation.

Provides a POST /simulate endpoint that accepts simulation parameters
as JSON and returns the generated plots as base64-encoded PNG images.
"""

import base64
import io

import matplotlib
matplotlib.use("Agg")

from flask import Flask, jsonify, render_template, request

from chemotaxis import ChemotaxisSimulator

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the main frontend page."""
    return render_template("index.html")


@app.route("/simulate", methods=["POST"])
def simulate():
    """Run a chemotaxis simulation and return the resulting plots.

    Accepts a JSON body with the following optional fields:
        num_steps (int): number of time-steps per trajectory (default 50)
        num_trajectories (int): number of trajectories to generate (default 10)
        step_size (float): distance per step (default 1.0)
        bounds (list): [min, max] for random starting positions (default [-10, 10])

    Returns a JSON object with two base64-encoded PNG strings:
        trajectories: 2D spatial plot of all trajectories
        concentration_vs_time: concentration at each time-step for each trajectory
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()

    # Validate num_steps
    num_steps = data.get("num_steps", 50)
    if not isinstance(num_steps, int) or num_steps < 1:
        return jsonify({"error": "num_steps must be a positive integer"}), 400

    # Validate num_trajectories
    num_trajectories = data.get("num_trajectories", 10)
    if not isinstance(num_trajectories, int) or num_trajectories < 1:
        return jsonify({"error": "num_trajectories must be a positive integer"}), 400

    # Validate step_size (accept int or float, must be positive)
    step_size = data.get("step_size", 1.0)
    if not isinstance(step_size, (int, float)) or step_size <= 0:
        return jsonify({"error": "step_size must be a positive number"}), 400

    # Validate bounds: must be a list of two numbers where min < max
    bounds = data.get("bounds", [-10, 10])
    if (not isinstance(bounds, list) or len(bounds) != 2
            or not all(isinstance(b, (int, float)) for b in bounds)
            or bounds[0] >= bounds[1]):
        return jsonify({"error": "bounds must be a list of two numbers [min, max] where min < max"}), 400

    # Run the simulation with the provided (or default) parameters
    sim = ChemotaxisSimulator(
        num_steps=num_steps,
        num_trajectories=num_trajectories,
        step_size=step_size,
        bounds=tuple(bounds),
    )
    sim.generate_trajectories()

    # Render the trajectory plot to an in-memory buffer
    buf1 = io.BytesIO()
    sim.plot_trajectories(save_path=buf1)
    buf1.seek(0)

    # Render the concentration-vs-time plot to an in-memory buffer
    buf2 = io.BytesIO()
    sim.plot_concentration_vs_time(save_path=buf2)
    buf2.seek(0)

    # Return both plots as base64-encoded PNG strings
    return jsonify({
        "trajectories": base64.b64encode(buf1.read()).decode("utf-8"),
        "concentration_vs_time": base64.b64encode(buf2.read()).decode("utf-8"),
    })
