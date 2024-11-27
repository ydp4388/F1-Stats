from celery import shared_task
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import datetime

channel_layer = get_channel_layer()

drivers = {1: "VER", 4: "NOR", 16: "LEC", 55: "SAI", 81: "PIA", 11: "PER", 63: "RUS", 44: "HAM", 14: "ALO", 18: "STR", 27: "HUL", 22: "TSU", 3: "RIC", 38: "BEA", 10: "GAS", 20: "MAG", 23: "ALB", 31: "OCO", 24: "ZHO", 2: "SAR", 77: "BOT"}
colors = {1: "rgb(51,51,255)", 4: "rgb(255,153,51)", 16: "rgb(255,0,0)", 55: "rgb(255,0,0)", 81: "rgb(255,153,51)", 11: "rgb(51,51,255)", 63: "rgb(160,160,160)", 44: "rgb(160,160,160)", 14: "rgb(0,102,0)", 18: "rgb(0,102,0)", 27: "rgb(255,204,204)", 22: "rgb(0,128,255)", 3: "rgb(0,128,255)", 38: "rgb(0,0,0)", 10: "rgb(0,0,0)", 20: "rgb(255,204,204)", 23: "rgb(0,76,153)", 31: "rgb(0,0,0)", 24: "rgb(0,255,0)", 2: "rgb(0,76,153)", 77: "rgb(0,255,0)"}

def parseData(text: str) -> json:
    result = {}

    try:
        data_list = eval(text.strip())

        # Initialize the result dictionary
        result = {
            "drivers": {},
            "timestamp": datetime.datetime.fromisoformat(data_list[2].rstrip('Z')).__str__()
        }

        if type(data_list[1]) is str:
            return result
        
        lines_data = data_list[1].get('Lines', {})


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
                        driver_info.get("stints")[stint] = {
                            "lap_number": stint_data['LapNumber'],
                            "lap_time": stint_data['LapTime']
                        }
            
            if driver_info.get("stints") and driver_info.get("stints") != {}:
                result.get("drivers")[driver_number] = driver_info
                
    except Exception as e:
        print(e)
        return result
    return result

@shared_task(ignore_result=True)
def add(where):
    with open("live_data/dataFiles/live_data_test.txt", "r") as file:
        if where is not None:
            file.seek(where)
        while True:
            data = file.readline()
            where = file.tell()
            if not data:
                # Reached the end of the file
                time.sleep(5)
                data = file.readline()
                if not data:
                    break
                add.delay(where)  # Reset file pointer to last reading line
            else:
                parsed_data = parseData(data)
                parsed_data = cleanData(parsed_data)
                if parsed_data.get("drivers") != {}:
                    async_to_sync(channel_layer.group_send)('chat_chat',{
                        "type": "chat_message",
                        "message": parsed_data
                    })
        async_to_sync(channel_layer.group_send)('chat_chat',{
                "type": "chat_message",
                "message": 'test123'
            }
        )

def cleanData(data: dict) -> dict:
    for key in list(data.get("drivers").keys()):
        if data.get("drivers").get(key) == {}:
            data.get("drivers").pop(key, None)
    return data

