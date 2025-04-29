import pandas as pd

# CSV file
df = pd.read_csv('bc_veh4223_230215.csv')

# Fix OPD_DATE format
df['OPD_DATE'] = df['OPD_DATE'].str.split(':').str[0]
df['OPD_DATE'] = pd.to_datetime(df['OPD_DATE'], format='%d%b%Y')

# TIMESTAMP = OPD_DATE + ACT_TIME
df['TIMESTAMP'] = df['OPD_DATE'] + pd.to_timedelta(df['ACT_TIME'], unit='s')

# Calculate dMETERS, dTIMESTAMP group by VEHICLE_ID and EVENT_NO_TRIP
df['dMETERS'] = df.groupby(['VEHICLE_ID', 'EVENT_NO_TRIP'])['METERS'].diff()
df['dTIMESTAMP'] = df.groupby(['VEHICLE_ID', 'EVENT_NO_TRIP'])['TIMESTAMP'].diff().dt.total_seconds()

# SPEED = dMETERS / dTIMESTAMP
df['SPEED'] = df.apply(lambda row: row['dMETERS'] / row['dTIMESTAMP'] if row['dTIMESTAMP'] != 0 else 0, axis=1)
df = df.dropna(subset=['SPEED']) # Drop any NULL value in SPEED

# Drop dMETERS and dTIMESTAMP
df = df.drop(columns=['dMETERS', 'dTIMESTAMP'])

# Test
print(df[['VEHICLE_ID', 'EVENT_NO_TRIP', 'TIMESTAMP', 'SPEED']].head())

# Select 02/15/2023
df = df[df['TIMESTAMP'].dt.date == pd.to_datetime('2023-02-15').date()]

# Calculate max speed
max_speed = df['SPEED'].max()
print(f"Maximum speed: {max_speed:.2f} meters/second")

max_speed_row = df[df['SPEED'] == max_speed]
print(max_speed_row[['TIMESTAMP', 'GPS_LATITUDE', 'GPS_LONGITUDE']])

# Calculate median speed
median_speed = df['SPEED'].median()
print(f"Median speed: {median_speed:.2f} meters/second")
