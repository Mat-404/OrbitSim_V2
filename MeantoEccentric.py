import math

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

def rad(deg):
    return deg * math.pi / 180

def deg(rad):
    return rad * 180 / math.pi

print(mean_to_eccentric(rad(45), .5))