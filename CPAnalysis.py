# Load the newly uploaded CSV file
# file_path = 'BTL inserts deviations 2024-7-23 scan 2 Z+ to Z- Row 1 to 38.csv'
# file_path = 'BTL insert deviations 2024-7-31 scan 3 Z+ to Z- Row 1 to 38.csv'
# file_path = 'BTL inserts deviations 2024-7-18 scan 1 Z+ to Z- Row 1 to 38.csv'
# file_path = 'BTL insert deviations 2024-7-23 nominals.csv'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file (adjust the file path as needed)
file_path = 'BTL insert deviations 2024-7-31 scan 3 Z+ to Z- Row 1 to 38.csv'
# Assign appropriate column headers and load data
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

# Define parameters
nominal_radius = 1191  # nominal radius in mm
tolerance = 1.5  # tolerance in mm

# Extract unique CP names (CP1, CP2, ..., CP18) for grouping
cp_names = sorted(data['Measurement_name'].unique())

# Plotting radius against Z position, grouping by CP number
plt.figure(figsize=(12, 8))

for cp in cp_names:
    # Filter data for the current CP
    cp_data = data[data['Measurement_name'] == cp]
    # Plot the radius for the CP, spanning all Z positions across rails
    plt.plot(cp_data['Z_position'], cp_data['Radius'], label=f'{cp}')

# Plot nominal radius and tolerance lines with increased thickness
plt.axhline(nominal_radius, color='gray', linestyle='--', linewidth=2, label='Nominal Radius')
plt.axhline(nominal_radius + tolerance, color='red', linestyle='--', linewidth=1.5, label='Tolerance')
plt.axhline(nominal_radius - tolerance, color='red', linestyle='--', linewidth=1.5)

# Adding labels and repositioning the legend
plt.xlabel('Z Position (mm)')
plt.ylabel('Radius (mm)')
plt.title('Radius of Tube vs. Z Position by CP Number')
plt.legend(title='CP', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=6)
plt.grid(True)
plt.tight_layout()
plt.show()
