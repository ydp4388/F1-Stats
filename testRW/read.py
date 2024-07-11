import time

with open("live_data.txt", "r") as file:
    while True:
        data = file.readline()
        where = file.tell()
        if not data:
            # Reached the end of the file
            time.sleep(0.1)  # Wait before checking again
            file.seek(where)  # Reset file pointer to the beginning
        else:
            print(data, end="")