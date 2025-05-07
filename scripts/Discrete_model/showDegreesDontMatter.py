import numpy as np

def lonlat_step_to_meters_simple(pos_old, pos_new):
    # Extract lon/lat in degrees
    lon0, lat0 = pos_old
    lon1, lat1 = pos_new

    # Average latitude in radians
    lat_avg_rad = np.radians((lat0 + lat1) / 2)

    # Degree differences
    dlon = lon1 - lon0
    dlat = lat1 - lat0

    # Approximate conversion constants
    meters_per_deg_lat = 111_320
    meters_per_deg_lon = 111_320 * np.cos(lat_avg_rad)

    # Convert to meters
    dx = dlon * meters_per_deg_lon
    dy = dlat * meters_per_deg_lat

    return np.array([dx, dy])

import numpy as np

# Define bounds
lat_min = 42.5
lat_max = 46.5

# Generate a range of latitudes to evaluate
latitudes_deg = np.linspace(lat_min, lat_max, 100)
latitudes_rad = np.radians(latitudes_deg)

# Approximate constants
meters_per_deg_lat = 111_320  # approximately constant
meters_per_deg_lon = 111_320 * np.cos(latitudes_rad)

# Compute min/max longitudinal step sizes
min_lon_step = np.min(meters_per_deg_lon)
max_lon_step = np.max(meters_per_deg_lon)

print(f"Minimum meters per degree longitude: {min_lon_step:.2f} m")
print(f"Maximum meters per degree longitude: {max_lon_step:.2f} m")
print(f"Meters per degree latitude (approx): {meters_per_deg_lat:.2f} m")
