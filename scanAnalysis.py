
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
num_cps_per_rail = 18  # number of CP measurements per rail
num_rails = len(data) // num_cps_per_rail  # total number of rails in the dataset

# Plotting radius against Z position for each rail
plt.figure(figsize=(12, 8))

for rail_num in range(num_rails):
    # Extract data for the current rail
    rail_data = data.iloc[rail_num * num_cps_per_rail:(rail_num + 1) * num_cps_per_rail]
    # Plot the radius against Z position for this rail
    plt.plot(rail_data['Z_position'], rail_data['Radius'], label=f'Rail {rail_num + 1}')

# Plot nominal radius and tolerance lines with increased thickness
plt.axhline(nominal_radius, color='gray', linestyle='--', linewidth=2, label='Nominal Radius')
plt.axhline(nominal_radius + tolerance, color='red', linestyle='--', linewidth=1.5, label='Tolerance')
plt.axhline(nominal_radius - tolerance, color='red', linestyle='--', linewidth=1.5)

# Adding labels and repositioning the legend
plt.xlabel('Z Position (mm)')
plt.ylabel('Radius (mm)')
plt.title('Radius of Tube vs. Z Position by Rail')
plt.legend(title='Rail', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=6)
plt.grid(True)
plt.tight_layout()
plt.show()

# Filter the data to include only points that are out of tolerance
out_of_tolerance = data[(data['Radius'] > nominal_radius + tolerance) | (data['Radius'] < nominal_radius - tolerance)]

# Add rail number column to identify the rail for each point based on the row position in the dataset
out_of_tolerance = out_of_tolerance.copy()
out_of_tolerance['Rail_Number'] = (out_of_tolerance.index // num_cps_per_rail) + 1

# Select and reorder relevant columns for the output table
out_of_tolerance_table = out_of_tolerance[
    ['Rail_Number', 'Measurement_name', 'Radius', 'X_position', 'Y_position', 'Z_position']
]

# Display the out-of-tolerance table
print("Out of Tolerance Points:")
print(out_of_tolerance_table)
