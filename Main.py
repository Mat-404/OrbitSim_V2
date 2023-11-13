import config
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

# Initialize the celestial data and time step
global config_list
global deltaT
if 'config_list' not in globals():
    config_list = config.main()
if 'deltaT' not in globals():
    deltaT = 3600 * 365.25 * 5  # 1 Earth year

# Define the bounds for X and Y axes
x_min, x_max = -800_000_000, 800_000_000
y_min, y_max = -800_000_000, 800_000_000

# Function to convert mean anomaly to eccentric anomaly
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


# Function to update the celestial bodies' positions
def update_data(frame):
    global config_list  # Declare config_list as a global variable
    global deltaT
    for i in config_list.keys():
        orbital_period = config_list[i]["Period"]
        delta_t = deltaT / orbital_period
        MeanAnomaly = 2 * math.pi * config_list[i]["t"]
        EccentricAnomaly = mean_to_eccentric(MeanAnomaly, config_list[i]["Eccentricity"])
        config_list[i]["Theta"] = 2 * math.atan(
            math.sqrt((1 + config_list[i]["Eccentricity"]) / (1 - config_list[i]["Eccentricity"])) *
            math.tan(EccentricAnomaly / 2)
        )
        r = config_list[i]["SemiMajorAxis"] * (1 - config_list[i]["Eccentricity"] ** 2) / (
                    1 + (config_list[i]["Eccentricity"]) * math.cos(config_list[i]["Theta"]))
        config_list[i]["XVals"].append(r * math.cos(config_list[i]["Theta"] + config_list[i]["Argument of Periapsis (radians)"]))
        config_list[i]["YVals"].append(r * math.sin(config_list[i]["Theta"] + config_list[i]["Argument of Periapsis (radians)"]))
        config_list[i]["t"] += delta_t

        # If the list of XVals becomes too long, remove the oldest data points
        if len(config_list[i]["XVals"]) > config_list[i]["Period"] / (365*24*3600):
            config_list[i]["XVals"].pop(0)
            config_list[i]["YVals"].pop(0)
        
        #print(config_list["Mars"]["Theta"] - config_list["Earth"]["Theta"])
        
        # Get angle between Earth and Mars
        if abs(config_list["Mars"]["Theta"] - config_list["Earth"]["Theta"]) > (44 * (math.pi / 180)) and not config_list["Transfer"]["Created"]:   
            config_list["Transfer"]["Apoapsis Radius (km)"] = config_list["Mars"]["SemiMajorAxis"] * (1 - config_list["Mars"]["Eccentricity"] ** 2) / (
                    1 + (config_list["Mars"]["Eccentricity"]) * math.cos(config_list["Mars"]["Theta"] + math.pi))
            config_list["Transfer"]["Periapsis Radius (km)"] = config_list["Earth"]["SemiMajorAxis"] * (1 - config_list["Earth"]["Eccentricity"] ** 2) / (
                    1 + (config_list["Earth"]["Eccentricity"]) * math.cos(config_list["Earth"]["Theta"]))
            config_list["Transfer"]["Argument of Periapsis (radians)"] = config_list["Earth"]["Theta"]
            config_list["Transfer"]["Theta"] = 0.00
            config_list["Transfer"]["t"] = 0.00
            config_list["Transfer"]["Eccentricity"] = (config_list["Transfer"]["Apoapsis Radius (km)"] - config_list["Transfer"]["Periapsis Radius (km)"]) / (config_list["Transfer"]["Apoapsis Radius (km)"] + config_list["Transfer"]["Periapsis Radius (km)"])
            config_list["Transfer"]["Created"] = True

        #if i == "Transfer":
        #    print(config_list["Transfer"])


    return config_list

# Function to animate the plot
def animate(frame):
    global config_list  # Declare config_list as a global variable
    config_list = update_data(frame)
    plt.cla()

    # Set a black background for the plot
    plt.gca().set_facecolor('black')

    # Plot the paths of all celestial bodies with legend
    for body in config_list.keys():
        if body != "Transfer":
            eccentricity = config_list[body]["Eccentricity"]
            label = f"{body} (Eccentricity: {eccentricity:.4f})"
            plt.plot(config_list[body]["XVals"], config_list[body]["YVals"], label=label)
        else:
            transfer = config_list["Transfer"]
            plt.plot(transfer["XVals"], transfer["YVals"], label="Transfer Orbit (Eccentricity: {:.4f})".format(transfer["Eccentricity"]), color='white')    

    # Set the X and Y-axis limits
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.gca().set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal

    # Set the color of the axes and text to white
    plt.xticks(color='white')
    plt.yticks(color='white')

    # Add epoch time as white text to the plot
    plt.text(-x_max * 0.5, y_max * 0.9, f'Epoch Time: {(frame * (deltaT * 3.70116e-7)):.0f} Earth Days', ha='right', va='top', color='white')

    # Set the title, labels, and legend text to white
    plt.title('Solar System Plot', color='white')
    plt.xlabel('X-Axis (km)', color='white')
    plt.ylabel('Y-Axis (km)', color='white')
    plt.legend(loc='upper right')

# Initialize the celestial bodies
for i in config_list.keys():
    config_list[i]["XVals"] = []
    config_list[i]["YVals"] = []
    config_list[i]["t"] = 0.00
    config_list[i]["Theta"] = 0.00
    config_list[i]["Period"] = 2 * math.pi * math.sqrt(config_list[i]["SemiMajorAxis"] ** 3 / config_list["Sun"]["Gravitational Parameter (km^3/s^2)"])

# Create the plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, animate, frames=1, interval=1)  # 1 second interval, 100 frames

# Show the plot
plt.tight_layout()
plt.show()
