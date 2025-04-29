import pandas as pd

# CSV file
df = pd.read_csv('bc_trip259172515_230215.csv')

# Count records
print(f"Number of records: {len(df)}")

# Drop EVENT_NO_STOP, GPS_SATELLITES, and GPS_HDOP
#df = df.drop(columns=['EVENT_NO_STOP', 'GPS_SATELLITES', 'GPS_HDOP'])

filtered_columns = [
    'EVENT_NO_TRIP', 'OPD_DATE', 'VEHICLE_ID', 
    'METERS', 'ACT_TIME', 'GPS_LONGITUDE', 'GPS_LATITUDE'
]

df = pd.read_csv('bc_trip259172515_230215.csv', usecols=filtered_columns)
#print(df.columns)

### DECODING ###

# Clean OPD_DATE and convert to the right format
df['OPD_DATE'] = df['OPD_DATE'].str.split(':').str[0]
df['OPD_DATE'] = pd.to_datetime(df['OPD_DATE'], format='%d%b%Y')

# TIMESTAMP = OPD_DATE + ACT_TIME
df['TIMESTAMP'] = df['OPD_DATE'] + pd.to_timedelta(df['ACT_TIME'], unit='s')

# Drop OBD_DATE and ACT_TIME
df = df.drop(columns=['OPD_DATE', 'ACT_TIME'])

print(df[['TIMESTAMP']].head())
#print(df.columns)

### ENHANCING ####

# dMETERS and dTIMESTAMP difference
df['dMETERS'] = df['METERS'].diff()

# dTIMESTAMP (in seconds)
df['dTIMESTAMP'] = df['TIMESTAMP'].diff().dt.total_seconds()

#print(df[['dMETERS', 'dTIMESTAMP']].head())

# SPEED = dMETERS / dTIMESTAMP
df['SPEED'] = df.apply(lambda row: row['dMETERS'] / row['dTIMESTAMP'] if row['dTIMESTAMP'] != 0 else 0, axis=1)
df = df.dropna(subset=['SPEED'])

# Drop dMETERS and dTIMESTAMP
df = df.drop(columns=['dMETERS', 'dTIMESTAMP'])

# Test
# print(df[['METERS', 'TIMESTAMP', 'SPEED']].head())

# Calculate max, min and avg speed
min_speed = df['SPEED'].min()
print(f"Minimum SPEED: {min_speed:.2f} m/s")

max_speed = df['SPEED'].max()
print(f"Maximum SPEED: {max_speed:.2f} m/s")

avg_speed = df['SPEED'].mean()
print(f"Average SPEED: {avg_speed:.2f} m/s")
