import pandas as pd

# Read the CSV files
df1 = pd.read_csv('marker_coordinates_1.csv')
df2 = pd.read_csv('marker_coordinates_2.csv')

# Merge based on timestamp
merged_df = pd.merge(df1, df2, on='Timestamp')

# Save the merged dataframe to a new CSV file
merged_df.to_csv('merged.csv', index=False)
