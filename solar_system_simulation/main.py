import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for animations

# Constants
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
AU = 1.496e11  # Astronomical unit in meters
DAY = 24 * 3600  # One day in seconds
SUN_MASS = 1.989e30  # Mass of the sun in kg

# Data for planets (mass in kg, distance from the sun in meters, velocity in m/s)
planets_data = {
    "Mercury": {"mass": 3.30e23, "distance": 0.39 * AU, "velocity": 47400, "color": "gray"},
    "Venus": {"mass": 4.87e24, "distance": 0.72 * AU, "velocity": 35000, "color": "yellow"},
    "Earth": {"mass": 5.97e24, "distance": 1.00 * AU, "velocity": 29783, "color": "blue"},
    "Mars": {"mass": 6.42e23, "distance": 1.52 * AU, "velocity": 24007, "color": "red"},
    "Jupiter": {"mass": 1.90e27, "distance": 5.20 * AU, "velocity": 13070, "color": "orange"},
    "Saturn": {"mass": 5.68e26, "distance": 9.58 * AU, "velocity": 9680, "color": "gold"},
    "Uranus": {"mass": 8.68e25, "distance": 19.18 * AU, "velocity": 6810, "color": "lightblue"},
    "Neptune": {"mass": 1.02e26, "distance": 30.07 * AU, "velocity": 5430, "color": "darkblue"}
}

# Initialize planet positions and velocities
planets = {}
for planet, data in planets_data.items():
    planets[planet] = {
        "pos": np.array([data["distance"], 0], dtype="float64"),
        "vel": np.array([0, data["velocity"]], dtype="float64"),
        "mass": data["mass"],
        "color": data["color"],
        "trail_x": [],  # To store x-coordinates for the orbit trail
        "trail_y": []  # To store y-coordinates for the orbit trail
    }


# Function to compute gravitational force
def gravitational_force(pos1, pos2, mass1, mass2):
    r = np.linalg.norm(pos2 - pos1)
    force = G * mass1 * mass2 / r ** 2
    direction = (pos2 - pos1) / r
    return force * direction


# Time step and simulation parameters
dt = DAY  # 1 day in seconds
total_time = 365 * DAY  # Simulate for one Earth year

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-35 * AU, 35 * AU)
ax.set_ylim(-35 * AU, 35 * AU)

# Plot sun
sun, = ax.plot(0, 0, 'yo', markersize=15, label='Sun')

# Create planet plots and trails
planet_plots = {}
trails = {}
for planet, data in planets_data.items():
    # Plot for the planet
    planet_plots[planet], = ax.plot([], [], 'o', color=data["color"], label=planet)
    # Line for the trail
    trails[planet], = ax.plot([], [], color=data["color"], lw=1)


# Update function for animation
def update(frame):
    for planet, data in planets.items():
        # Calculate the force from the Sun
        force_sun = gravitational_force(np.array([0, 0]), data["pos"], data["mass"], SUN_MASS)
        acceleration = force_sun / data["mass"]
        data["vel"] += acceleration * dt
        data["pos"] += data["vel"] * dt

        # Update planet position
        planet_plots[planet].set_data(data["pos"][0], data["pos"][1])

        # Store the trail positions
        data["trail_x"].append(data["pos"][0])
        data["trail_y"].append(data["pos"][1])
        trails[planet].set_data(data["trail_x"], data["trail_y"])

    return [planet_plots[planet] for planet in planets] + [trails[planet] for planet in planets]


# Animation setup with a faster interval
ani = FuncAnimation(fig, update, frames=int(total_time / dt), interval=10, blit=True)  # Adjusted interval

# Show legend
ax.legend()

# Display animation
plt.show()


