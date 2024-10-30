from celery import shared_task
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import datetime

def parseData(text: str) -> json:
    # # Initialize the result dictionary
    # result = {
    #     "drivers": {},
    #     "timestamp": datetime.date.fromisoformat(data_list[2].rstrip('Z'))
    # }
    result = {}

    try:
        print(text[1])
        data_list = eval(text.strip())

        print(data_list[2].rstrip('Z'))

        # Initialize the result dictionary
        result = {
            "drivers": {},
            "timestamp": datetime.datetime.fromisoformat(data_list[2].rstrip('Z'))
        }

        lines_data = data_list[1]['Lines']


        for driver_number, driver_data in lines_data.items():
            driver_name = "UNK"
            driver_color = 'rgb(0,0,0)'
            driver_info = {}
            if int(driver_number) in drivers.keys():
                dr_name = drivers.get(int(driver_number))
                dr_color = colors.get(int(driver_number))
            
            if 'Stints' in driver_data:
                driver_info["stints"] = {}
                for stint, stint_data in driver_data['Stints'].items():
                    if 'LapTime' in stint_data:
                        driver_info["stints"][stint] = {
                            "lap_number": stint_data['LapNumber'],
                            "lap_time": stint_data['LapTime']
                        }
            
            result["drivers"][driver_number] = driver_info
        print("End")
                
    except Exception as e:
        print(e)
        return result
    return result

data = "['TimingAppData', {'Lines': {'24': {'Line': 13, 'Stints': {'0': {'LapTime': '1:32.751', 'LapNumber': 4}}}, '61': {'Line': 14}}}, '2024-07-05T11:37:41.812Z']"
parsed = parseData(data)
print(parsed)