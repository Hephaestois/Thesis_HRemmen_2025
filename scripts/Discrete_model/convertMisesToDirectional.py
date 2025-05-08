import numpy as np
from scipy.stats import vonmises
from scipy.integrate import quad

def wrap_angle(theta):
    """Wrap angle to [-π, π]."""
    return ((theta + np.pi) % (2 * np.pi)) - np.pi

def integrate_sector(mu, kappa, a, b):
    """Integrate the von Mises distribution from angle a to b."""
    # Ensure correct ordering
    if a < b:
        result, _ = quad(lambda theta: vonmises.pdf(theta, kappa, loc=mu), a, b)
    else:
        # Handle wrapping across -π/π boundary
        result1, _ = quad(lambda theta: vonmises.pdf(theta, kappa, loc=mu), a, np.pi)
        result2, _ = quad(lambda theta: vonmises.pdf(theta, kappa, loc=mu), -np.pi, b)
        result = result1 + result2
    return result

def vonmises_to_lrud(mu, kappa):
    """Convert von Mises distribution to LRUD probabilities."""
    # Define sector boundaries (centered on cardinal directions)
    bounds = {
        'r': (wrap_angle(-np.pi/4), wrap_angle(np.pi/4)),
        'u': (wrap_angle(np.pi/4), wrap_angle(3*np.pi/4)),
        'l': (wrap_angle(3*np.pi/4), wrap_angle(-3*np.pi/4)),
        'd': (wrap_angle(-3*np.pi/4), wrap_angle(-np.pi/4)),
    }

    # Integrate over each sector
    probabilities = {dir: integrate_sector(mu, kappa, *bounds[dir]) for dir in bounds}
    return probabilities

# Example: mean direction = 0 (east), kappa = 2
mu = 5.0233 # radians, direction of v
kappa = 0.874

lrud_probs = vonmises_to_lrud(mu, kappa)
print(lrud_probs)
