import time
import json

buffsize = 1
with open("live_data.txt", "r") as rFile:
    with open("live_data_test.txt", "w", buffering=buffsize) as wFile:
        while True:
            data = rFile.readline()
            wFile.write(data)
            data = data.replace('[', '').replace(']', '').split(',')
            print(data[0].strip('\''))
            # if data[0].strip('\'') == 'TimingData':
            print(type(data[1].strip()))
            val = eval(data[1].strip())
            # print(val.get('Lines'))
            print(type(val))
            time.sleep(1)