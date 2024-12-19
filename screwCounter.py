
# Load the newly uploaded CSV file
# file_path = 'BTL inserts deviations 2024-7-23 scan 2 Z+ to Z- Row 1 to 38.csv'
# file_path = 'BTL insert deviations 2024-7-31 scan 3 Z+ to Z- Row 1 to 38.csv'
# file_path = 'BTL inserts deviations 2024-7-18 scan 1 Z+ to Z- Row 1 to 38.csv'
# file_path = 'BTL insert deviations 2024-7-23 nominals.csv'
import pandas as pd
import numpy as np
import math
from collections import Counter

# Load the CSV file (adjust the file path as needed)
file_path = 'BTL inserts deviations 2024-7-23 scan 2 Z+ to Z- Row 1 to 38.csv'
columns = [
    "Measurement_type", "Measurement_name", "X_position", "Y_position", "Z_position",
    "i_component", "j_component", "k_component"
]
data = pd.read_csv(file_path, sep=';', names=columns, skiprows=1, engine='python')

# Convert columns to numeric, replacing commas
data['X_position'] = pd.to_numeric(data['X_position'].str.replace(',', ''), errors='coerce')
data['Y_position'] = pd.to_numeric(data['Y_position'].str.replace(',', ''), errors='coerce')
data['Z_position'] = pd.to_numeric(data['Z_position'].str.replace(',', ''), errors='coerce')

# Calculate the radius for each point
data['Radius'] = np.sqrt(data['X_position']**2 + data['Y_position']**2)

# Constants
target_radius = 1149.0  # Target radius in mm
nominal_radius = 1191.0  # Nominal radius in mm
tolerance = 1.5  # Tolerance in mm
additional_length_6mm = 39.8  # Length of rail + 6mm feet
additional_length_4mm = 37.8  # Length of rail + 4mm feet

# Prepare counters for screws and feet
screw_adjustments_4mm = Counter()
screw_adjustments_6mm = Counter()
feet_4mm_needed = 0
feet_6mm_needed = 0
screws_to_purchase = Counter({'4mm': 80, '6mm': 80, '8mm': 80})  # Start with 80 spare screws per type

# Process each radius point
for index, row in data.iterrows():
    radius = row['Radius']
    adjusted_radius_with_6mm = radius - additional_length_6mm
    adjusted_radius_with_4mm = radius - additional_length_4mm

    # Check if radius is below the tolerance limit
    if radius <= (nominal_radius - tolerance):
        # Use 4mm feet
        feet_4mm_needed += 1
        required_adjustment = adjusted_radius_with_4mm - target_radius
        screw_size = (
            '4mm' if required_adjustment <= 2 else 
            '6mm' if 2 < required_adjustment <= 4 else 
            '8mm'
        )
        # Record screw adjustment for 4mm feet
        required_adjustment = math.floor(required_adjustment * 10) / 10.0
        if required_adjustment > 0:
            screw_adjustments_4mm[required_adjustment] += 4  # 4 screws per foot

    else:
        # Use 6mm feet if within tolerance
        feet_6mm_needed += 1
        required_adjustment = adjusted_radius_with_6mm - target_radius
        screw_size = '6mm' if required_adjustment < 3 else '8mm'
        # Record screw adjustment for 6mm feet
        required_adjustment = math.floor(required_adjustment * 10) / 10.0
        if required_adjustment > 0:
            screw_adjustments_6mm[required_adjustment] += 4  # 4 screws per foot

    # Update screws to purchase
    screws_to_purchase[screw_size] += 4

# Display results
print("Screw Adjustment Requirements (multiplied by 4 per foot):")
print("4mm Feet:")
for length, count in sorted(screw_adjustments_4mm.items()):
    print(f"{count} screws of {length} mm adjustment")

print("\n6mm Feet:")
for length, count in sorted(screw_adjustments_6mm.items()):
    print(f"{count} screws of {length} mm adjustment")

print(f"\nFeet Requirements:")
print(f"{feet_6mm_needed} feet of 6 mm (subtracting 39.8 mm)")
print(f"{feet_4mm_needed} feet of 4 mm (subtracting 37.8 mm)")

print("\nScrew Purchase Requirements (including 80 spare screws for each size):")
for screw_type, count in screws_to_purchase.items():
    print(f"{count} screws of {screw_type} length")
