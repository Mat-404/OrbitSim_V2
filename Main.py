import config
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

global config_list
global deltaT
if 'config_list' not in globals():
    config_list = config.main()
if 'deltaT' not in globals():
    deltaT = 3600*365.25*4
# Define the bounds for X and Y axes
x_min, x_max = -3000_000_000, 3000_000_000  # Modify these values as needed
y_min, y_max = -3000_000_000, 3000_000_000  # Modify these values as needed



def mean_to_eccentric(mean_anomaly, eccentricity):
    # Ensure the eccentricity is within bounds
    eccentricity = max(0.0, min(1.0, eccentricity))

    # Maximum number of iterations and tolerance for convergence
    max_iterations = 100
    tolerance = 1e-8

    # Adjust the mean anomaly to be within [0, 2π)
    mean_anomaly = mean_anomaly % (2 * math.pi)

    # Initial guess: Start close to mean anomaly
    if eccentricity < 0.8:
        initial_guess = mean_anomaly
    else:
        initial_guess = math.pi
    for _ in range(max_iterations):
        E = initial_guess
        for _ in range(max_iterations):
            f = E - eccentricity * math.sin(E) - mean_anomaly
            f_prime = 1 - eccentricity * math.cos(E)
            E_new = E - f / f_prime
            # Check for convergence
            if abs(E_new - E) < tolerance:
                return E_new
            E = E_new
        # If it doesn't converge, improve the initial guess and retry
        if eccentricity < 0.8:
            initial_guess += 0.1  # Adjust the initial guess
        else:
            initial_guess = math.pi  # Start with a known good guess
    # If still not converged after retries, return None or handle appropriately
    return None

def update_data(frame):
    global config_list  # Declare config_list as a global variable
    global deltaT
    for i in config_list.keys():
        orbital_period = config_list[i]["Period"]
        delta_t = deltaT / orbital_period
        MeanAnomaly = 2 * math.pi * config_list[i]["t"]
        EccentricAnomaly = mean_to_eccentric(MeanAnomaly, config_list[i]["Eccentricity"])
        TrueAnomaly = 2 * math.atan(math.sqrt((1 + config_list[i]["Eccentricity"]) / (1 - config_list[i]["Eccentricity"])) * math.tan(EccentricAnomaly / 2))
        r = config_list[i]["SemiMajorAxis"] * (1 - config_list[i]["Eccentricity"] ** 2) / (1 + (config_list[i]["Eccentricity"]) * math.cos(TrueAnomaly))
        config_list[i]["XVals"].append(r * math.cos(TrueAnomaly + config_list[i]["Argument of Periapsis (radians)"]))
        config_list[i]["YVals"].append(r * math.sin(TrueAnomaly + config_list[i]["Argument of Periapsis (radians)"]))
        config_list[i]["t"] += delta_t
        print(frame)
        if TrueAnomaly < 0.2 and TrueAnomaly > -.2:
            config_list[i]["XVals"].clear()
            config_list[i]["YVals"].clear()
    return config_list


def animate(frame):
    global config_list  # Declare config_list as a global variable
    config_list = update_data(frame)
    plt.cla()
    
    # Plot the paths of all celestial bodies with legend
    for body in config_list.keys():
        eccentricity = config_list[body]["Eccentricity"]
        label = f"{body} (Eccentricity: {eccentricity:.4f})"
        plt.plot(config_list[body]["XVals"], config_list[body]["YVals"], label=label)
    
    # Set the X and Y-axis limits
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    
    plt.gca().set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal
    
    # Add epoch time as text to the plot
    plt.text(-x_max * 0.5, y_max * 0.9, f'Epoch Time: {(frame *(deltaT*3.70116e-7)):.0f} Earth Days', ha='right', va='top')
    
    plt.title('Solar System Plot')
    plt.xlabel('X-Axis (km)')
    plt.ylabel('Y-Axis (km)')
    plt.legend(loc='upper right')


for i in config_list.keys():
    config_list[i]["Eccentricity"] = (config_list[i]["Apoapsis Radius (km)"] - config_list[i]["Periapsis Radius (km)"]) / (config_list[i]["Apoapsis Radius (km)"] + config_list[i]["Periapsis Radius (km)"])
    config_list[i]["SemiMajorAxis"] = (config_list[i]["Apoapsis Radius (km)"] + config_list[i]["Periapsis Radius (km)"]) / 2
    config_list[i]["XVals"] = []
    config_list[i]["YVals"] = []
    config_list[i]["t"] = 0
    config_list[i]["Period"] = 2 * math.pi * math.sqrt(config_list[i]["SemiMajorAxis"] ** 3 / config_list["Sun"]["Gravitational Parameter (km^3/s^2)"])

fig, ax = plt.subplots()

ani = animation.FuncAnimation(fig, animate, frames=100000, interval=1)  # 1 second interval, 100 frames

# Show the plot
plt.tight_layout()
plt.show()
