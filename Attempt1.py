import config
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

global config_list
if 'config_list' not in globals():
    config_list = config.main()

# Define the bounds for X and Y axes
x_min, x_max = -2000_000_000, 2000_000_000  # Modify these values as needed
y_min, y_max = -2000_000_000, 2000_000_000  # Modify these values as needed

def update_data():
    global config_list  # Declare config_list as a global variable
    for i in config_list.keys():
        r = config_list[i]["SemiMajorAxis"] * (1 - config_list[i]["Eccentricity"]**2) / (1 + (config_list[i]["Eccentricity"]) * math.cos(config_list[i]["Theta"]))
        config_list[i]["XVals"].append(r * math.cos(config_list[i]["Theta"] ))
        config_list[i]["YVals"].append(r * math.sin(config_list[i]["Theta"] ))
        config_list[i]["Theta"] += math.pi / 100
    return config_list  

def animate(frame):
    global config_list  # Declare config_list as a global variable
    config_list = update_data()
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
    
    plt.title('Solar System Plot')
    plt.xlabel('X-Axis (km)')
    plt.ylabel('Y-Axis (km)')
    plt.legend(loc='upper right')

for i in config_list.keys():
    config_list[i]["Eccentricity"] = (config_list[i]["Apoapsis Radius (km)"] - config_list[i]["Periapsis Radius (km)"]) / (config_list[i]["Apoapsis Radius (km)"] + config_list[i]["Periapsis Radius (km)"])
    config_list[i]["SemiMajorAxis"] = (config_list[i]["Apoapsis Radius (km)"] + config_list[i]["Periapsis Radius (km)"]) / 2
    config_list[i]["XVals"] = []
    config_list[i]["YVals"] = []
    config_list[i]["Theta"] = 0

fig, ax = plt.subplots()

ani = animation.FuncAnimation(fig, animate, frames=(round(100*math.pi)), interval=1)  # 1 second interval, 100 frames

# Show the plot
plt.tight_layout()
plt.show()
