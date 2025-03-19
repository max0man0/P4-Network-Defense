import pandas as pd
from pathlib import Path
import numpy as np

NETWORK_NAMES = ("Organization 2 Network", "Organization 3 Network", "Residence 1 Network", "Residence 2 Network", "Residence 3 Network")

# List all the CSV files
csv_files = [Path("csv") / f"register_values{i}.csv" for i in range(1, 6)]

# Initialize a dataframe to hold combined data
combined_df = pd.DataFrame()

# Read all the CSV files and merge data
for i, file in enumerate(csv_files):
    df = pd.read_csv(file)
    combined_df[f"Ingress Prossessing Duration {i+1}"] = df[f"Ingress Prossessing Duration"]

## Add a network column where the values are: the first 20 rows are "Organization 2 Network", the next 20 rows are "Organization 3 Network", and so on
## and loop back to the first network after the last network until all rows are filled
# Get the number of rows in the dataframe
num_rows = combined_df.shape[0]

# Initialize list to hold the network names
network_column = []
    
# Loop through the network names and add them to the list
for i in range(0, num_rows):
    network_index = i // 20 % len(NETWORK_NAMES)
    network_column.append(NETWORK_NAMES[network_index])

# Add the network column to the dataframe
combined_df["Network"] = network_column

# Calculate the average
combined_df["Average Ingress Prossessing Duration"] = combined_df.filter(like="Ingress Prossessing Duration").mean(axis=1)


# Save the result to an Excel file
output_file = Path("csv") / "average_processing_duration_with_network.xlsx"
combined_df.to_excel(output_file, index=False)

print(f"Averaged processing durations saved to {output_file}")
