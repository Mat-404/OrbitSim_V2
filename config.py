from celestial_data import celestial_data
import math

def calculate_orbital_parameters(entry):
    parameters = {}

    if entry in celestial_data:
        body_data = celestial_data[entry]

        if body_data.get("Shape") == "Circle":
            parameters["Eccentricity"] = 0  
            parameters["SemiMajorAxis"] = body_data.get("Periapsis Radius (km)")
        if body_data.get("Shape") == "Ellipse":
            parameters["Eccentricity"] = (body_data.get("Apoapsis Radius (km)") - body_data.get("Periapsis Radius (km)")) / (body_data.get("Apoapsis Radius (km)") + body_data.get("Periapsis Radius (km)"))
            parameters["SemiMajorAxis"] = (body_data.get("Periapsis Radius (km)") + body_data.get("Apoapsis Radius (km)")) / 2
        if body_data.get("Shape") == "Parabola":
            parameters["Eccentricity"] = 1
        if body_data.get("Shape") == "Hyperbola":
            parameters["EscapeVel"] = math.sqrt(2 * 1.3271244e8 / body_data.get("Periapsis Radius (km)"))

        parameters.update(body_data)  # Include other parameters from celestial_data
    
    else:
        parameters = {"Error": "Entry not found"}

    return parameters

def main():
    bodies = ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Transfer", "PSYCHE", "2P/Encke"]
    config_data = {body: calculate_orbital_parameters(body) for body in bodies}
    return config_data

if __name__ == "__main__":
    config = main()