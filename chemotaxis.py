"""
Simulate chemotaxis of E. coli in a 2D grid.

The key parameter is "concentration", defined here as the negative of the
distance from the food source at the origin.  A higher (less negative)
concentration means the cell is closer to the food.

Each time-step the cell takes a single step.  The step is either:
  - a "run": continue moving in the current direction, taken when
    concentration is increasing (i.e. moving toward the food source), or
  - a "tumble": pick a new random direction and step, taken when
    concentration is decreasing (i.e. moving away from the food source).

Usage:
    sim = ChemotaxisSimulator(num_steps=50, num_trajectories=10)
    sim.plot_trajectories()
"""

import math
import random

import matplotlib.pyplot as plt


class ChemotaxisSimulator:
    def __init__(self, num_steps, num_trajectories=1, step_size=1.0, bounds=(-10, 10)):
        """Create a new simulator.

        Args:
            num_steps: number of time-steps per trajectory.
            num_trajectories: number of trajectories to generate.
            step_size: distance travelled in a single step.
            bounds: (min, max) range for random starting positions on each axis.
        """
        self.num_steps = num_steps
        self.num_trajectories = num_trajectories
        self.step_size = step_size
        self.bounds = bounds
        self.trajectories = None
        self.concentrations_of_trajectories = None

    def get_concentration(self, x, y):
        """Return the concentration at position (x, y).

        Defined as the negative Euclidean distance from the origin (food source).
        Higher (less negative) values indicate proximity to food.
        """
        return -math.sqrt(x**2 + y**2)

    def run(self, x, y, direction):
        """Perform a run: continue straight in the current direction."""
        x += self.step_size * math.cos(direction)
        y += self.step_size * math.sin(direction)
        return x, y, direction

    def tumble(self, x, y):
        """Perform a tumble: pick a new random direction and step."""
        direction = random.uniform(0, 2 * math.pi)
        x += self.step_size * math.cos(direction)
        y += self.step_size * math.sin(direction)
        return x, y, direction

    def _generate_single_trajectory(self):
        """Generate a single trajectory starting from a random position.

        Returns a tuple of (trajectory, concentrations) where trajectory is
        a list of (x, y) tuples of length num_steps + 1 (including the
        starting position), and concentrations is a list of concentration
        values at each point on the trajectory.
        """
        x = random.uniform(*self.bounds)
        y = random.uniform(*self.bounds)
        direction = random.uniform(0, 2 * math.pi)
        trajectory = [(x, y)]
        concentrations = [self.get_concentration(x, y)]
        prev_concentration = concentrations[0]

        for _ in range(self.num_steps):
            # Get last element of concentrations list
            current_concentration = concentrations[-1]
            # Run when concentration is increasing (moving toward food),
            # tumble when it is decreasing (moving away).
            if current_concentration > prev_concentration:
                x, y, direction = self.run(x, y, direction)
            else:
                x, y, direction = self.tumble(x, y)
            prev_concentration = current_concentration
            trajectory.append((x, y))
            concentrations.append(self.get_concentration(x, y))

        return trajectory, concentrations

    def generate_trajectories(self):
        """Generate multiple trajectories and store them in self.trajectories.

        Also stores concentrations per trajectory in
        self.concentrations_of_trajectories.

        Returns a list of trajectories, each a list of (x, y) tuples.
        The number of trajectories is set by num_trajectories in the constructor.
        """
        results = [self._generate_single_trajectory() for _ in range(self.num_trajectories)]
        self.trajectories = [r[0] for r in results]
        self.concentrations_of_trajectories = [r[1] for r in results]
        return self.trajectories

    def plot_trajectories(self, show_average=True, save_path=None):
        """Generate and plot all trajectories on a 2D axes.

        Args:
            show_average: if True and num_trajectories > 1, also draw the
                mean trajectory as a dashed black line.
            save_path: if provided, save the figure to this path instead of
                calling plt.show().
        """
        if self.trajectories is None:
            self.generate_trajectories()
        trajectories = self.trajectories
        fig, ax = plt.subplots()
        for traj in trajectories:
            xs, ys = zip(*traj)
            ax.plot(xs, ys, alpha=0.5)

        if show_average and len(trajectories) > 1:
            max_len = max(len(t) for t in trajectories)
            avg_xs = []
            avg_ys = []
            for i in range(max_len):
                xs = [t[i][0] for t in trajectories if i < len(t)]
                ys = [t[i][1] for t in trajectories if i < len(t)]
                avg_xs.append(sum(xs) / len(xs))
                avg_ys.append(sum(ys) / len(ys))
            ax.plot(avg_xs, avg_ys, color='black', linewidth=2, linestyle='--', label='Average')
            ax.legend()

        ax.set_aspect('equal')
        ax.set_title('E. coli Chemotaxis Trajectories')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True)
        if save_path:
            fig.savefig(save_path)
            plt.close(fig)
        else:
            plt.show()

    def plot_concentration_vs_time(self, show_average=True, save_path=None):
        """Plot negative concentration vs time for all trajectories.

        Uses the concentrations stored in self.concentrations_of_trajectories.
        Generates trajectories first if they have not been generated yet.

        Args:
            show_average: if True and num_trajectories > 1, also draw the
                mean concentration over time as a dashed black line.
            save_path: if provided, save the figure to this path instead of
                calling plt.show().
        """
        if self.trajectories is None:
            self.generate_trajectories()

        fig, ax = plt.subplots()
        time_steps = list(range(len(self.concentrations_of_trajectories[0])))

        for conc in self.concentrations_of_trajectories:
            ax.plot(time_steps, conc, alpha=0.5)

        if show_average and len(self.concentrations_of_trajectories) > 1:
            max_len = max(len(c) for c in self.concentrations_of_trajectories)
            avg_conc = []
            for i in range(max_len):
                vals = [c[i] for c in self.concentrations_of_trajectories if i < len(c)]
                avg_conc.append(sum(vals) / len(vals))
            ax.plot(range(max_len), avg_conc, color='black', linewidth=2, linestyle='--', label='Average')
            ax.legend()

        ax.set_title('Concentration vs Time')
        ax.set_xlabel('Time step')
        ax.set_ylabel('Concentration (negative distance)')
        ax.grid(True)
        if save_path:
            fig.savefig(save_path)
            plt.close(fig)
        else:
            plt.show()
