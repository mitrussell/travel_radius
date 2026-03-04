import pandas as pd
import csv

# Estimated lat/long for each rack location based on city names
rack_locations = {
    'Phoenix, AZ': (33.4484, -112.0740),
    'Tucson, AZ': (32.2226, -110.9747),
    'Ciniza, NM': (35.0853, -106.6056),
    'Las Vegas, NV': (36.1699, -115.1398),
    'Cedar City, UT': (37.6775, -113.0619),
    'Imperial, CA': (32.8473, -115.5694),
    'Bloomfield, NM': (36.7067, -107.9848),
    'Stockton, CA': (37.9577, -121.2908),
    'Los Angeles, CA': (34.0522, -118.2437),
    'Barstow, CA': (34.8958, -117.0228),
    'Chico, CA': (39.7285, -121.8375),
    'Colton, CA': (34.0540, -117.3136),
    'Fresno, CA': (36.7378, -119.7871),
    'San Francisco, CA': (37.7749, -122.4194),
    'Orange, CA': (33.7879, -117.8531),
    'San Diego, CA': (32.7157, -117.1611),
    'Sacramento, CA': (38.5816, -121.4944),
    'San Jose, CA': (37.3382, -121.8863),
    'Bakersfield, CA': (35.3733, -119.0187),
    'Brisbane, CA': (37.6808, -122.4000),
    'Albuquerque, NM': (35.0844, -106.6504),
    'El Paso, TX': (31.7619, -106.4850),
    'Sparks/Reno, NV': (39.5296, -119.8138),
    'Eureka, CA': (40.8021, -124.1637),
    'Needles, CA': (34.8480, -114.6144),
    'Yuma, AZ': (32.6927, -114.6277),
    'Flagstaff, AZ': (35.1983, -111.6513),
    'Gallup, NM': (35.5281, -108.7426)
}

# Write to CSV
with open('rack_locations.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['rack_name', 'latitude', 'longitude'])
    for name, (lat, lon) in sorted(rack_locations.items()):
        writer.writerow([name, lat, lon])

print(f"Generated rack_locations.csv with {len(rack_locations)} locations")

# Create SVG map
min_lat = min(lat for lat, lon in rack_locations.values())
max_lat = max(lat for lat, lon in rack_locations.values())
min_lon = min(lon for lat, lon in rack_locations.values())
max_lon = max(lon for lat, lon in rack_locations.values())

width, height = 800, 600
margin = 50

def project(lat, lon):
    x = margin + (lon - min_lon) / (max_lon - min_lon) * (width - 2 * margin)
    y = height - margin - (lat - min_lat) / (max_lat - min_lat) * (height - 2 * margin)
    return x, y

svg_lines = [
    f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
    '<rect width="100%" height="100%" fill="white"/>',
]

for name, (lat, lon) in rack_locations.items():
    x, y = project(lat, lon)
    svg_lines.append(f'<circle cx="{x}" cy="{y}" r="5" fill="red"/>')
    svg_lines.append(f'<text x="{x+8}" y="{y+4}" font-size="10" fill="black">{name}</text>')

svg_lines.append('</svg>')

with open('rack_locations_map.svg', 'w') as f:
    f.write('\n'.join(svg_lines))

print("Generated rack_locations_map.svg")
