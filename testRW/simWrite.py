import time

bufsize = 1
with open("live_data.txt", "r") as rFile:
    with open("test_data.txt", "w", buffering=bufsize) as wFile:
        while True:
            data = rFile.readline()
            wFile.write(data)
            time.sleep(1)
