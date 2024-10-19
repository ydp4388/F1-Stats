# import time

# with open("live_data.txt", "r") as file:
#     while True:
#         data = file.readline()
#         where = file.tell()
#         if not data:
#             # Reached the end of the file
#             time.sleep(0.1)  # Wait before checking again
#             file.seek(where)  # Reset file pointer to the beginning
#         else:
#             print(data, end="")


import json
from datetime import datetime

# The string representation of the data
data_string = "['TimingAppData', {'Lines': {'1': {'Stints': {'0': {'TotalLaps': 3}}}, '63': {'Stints': {'2': {'TotalLaps': 3}}}}}, '2024-07-05T11:37:03.008Z']"

# Convert string to a list
data_list = eval(data_string)

# Extract the dictionary containing the Lines data
lines_data = data_list[1]['Lines']

# Parse driver numbers and lap times
for driver_number, driver_data in lines_data.items():
    print(f"Driver number: {driver_number}")
    
    if 'Stints' in driver_data:
        for stint, stint_data in driver_data['Stints'].items():
            if 'LapTime' in stint_data:
                print(f"  Stint {stint}: Lap {stint_data['LapNumber']}, Time: {stint_data['LapTime']}")
    else:
        print("  No lap time data available")

# Parse the timestamp
timestamp = datetime.fromisoformat(data_list[2].rstrip('Z'))
print(f"\nTimestamp: {timestamp}")