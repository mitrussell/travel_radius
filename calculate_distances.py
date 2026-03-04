import pandas as pd
from scgraph.geograph import haversine

# Read input files
df = pd.read_excel('CA_NV_AZ_Stations_WithPrimaryandSecondaryRacks_061621.xlsx')
racks = pd.read_csv('rack_locations.csv')

# Create rack lookup dictionary
rack_dict = {row['rack_name']: (row['latitude'], row['longitude']) 
             for _, row in racks.iterrows()}

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in miles using scgraph"""
    if pd.isna(lat1) or pd.isna(lon1) or pd.isna(lat2) or pd.isna(lon2):
        return None
    return haversine([lat1, lon1], [lat2, lon2], units='mi')

# Calculate distances
primary_distances = []
secondary_distances = []

for _, row in df.iterrows():
    station_lat = row['Latitude']
    station_lon = row['Longitude']
    
    # Primary rack distance
    primary_rack = row['PrimaryRack_Name']
    if pd.notna(primary_rack) and primary_rack in rack_dict:
        rack_lat, rack_lon = rack_dict[primary_rack]
        dist = calculate_distance(station_lat, station_lon, rack_lat, rack_lon)
        primary_distances.append(dist)
    else:
        primary_distances.append(None)
    
    # Secondary rack distance
    secondary_rack = row['SecondayRack_NAME']
    if pd.notna(secondary_rack) and secondary_rack in rack_dict:
        rack_lat, rack_lon = rack_dict[secondary_rack]
        dist = calculate_distance(station_lat, station_lon, rack_lat, rack_lon)
        secondary_distances.append(dist)
    else:
        secondary_distances.append(None)

# Add distance columns
df['distance_to_primary_rack_miles'] = primary_distances
df['distance_to_secondary_rack_miles'] = secondary_distances

# Write to CSV
df.to_csv('stations_with_distances.csv', index=False)

print(f"Processed {len(df)} stations")
print(f"Primary distances calculated: {sum(pd.notna(primary_distances))}")
print(f"Secondary distances calculated: {sum(pd.notna(secondary_distances))}")
print("Output written to stations_with_distances.csv")
