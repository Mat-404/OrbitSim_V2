from celestial_data import celestial_data

def get_celestial_data(entries):
    data = {}
    for entry in entries:
        if entry in celestial_data:
            data[entry] = celestial_data[entry]
        else:
            data[entry] = "Entry not found"

    return data

def main():
    bodies = ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "PSYCHE", "2P/Encke", "Transfer"]
    config_data = get_celestial_data(bodies)  # Rename the variable
    return config_data

print(main())

if __name__ == "__main__":
    config = main()
