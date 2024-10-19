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
    # Initialize the result dictionary
    result = {
        "drivers": {},
        "timestamp": datetime.fromisoformat(data_list[2].rstrip('Z'))
    }

    try:
        data_list = eval(text[1].strip())

        lines_data = data_list[1]['Lines']


        for driver_number, driver_data in lines_data.items():
            driver_name = "UNK"
            driver_color = 'rgb(0,0,0)'
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
                
    except:
        return result
    return result

@shared_task
def add(x, y, channel):
    with open("./dataFiles/live_data_test.txt", "r") as file:
        while True:
            data = file.readline()
            where = file.tell()
            if not data:
                # Reached the end of the file
                time.sleep(0.1)  # Wait before checking again
                file.seek(where)  # Reset file pointer to the beginning
            else:
                async_to_sync(channel_layer.group_send)('chat_chat',{
                    "type": "chat_message",
                    "message": data
                }
            )
        # print('elo')
        async_to_sync(channel_layer.group_send)('chat_chat',{
                "type": "chat_message",
                "message": 'test123'
            }
        )
    # print(x)
    # print('there')
                # print(data, end="")
    # async_to_sync(channel_layer.group_send)('chat_chat',{
    #         "type": "chat_message",
    #         "message": 'test123'
    #     }
    # )
    # print('sent')
    # return x + y
