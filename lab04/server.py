import os
import errno
import time
database = {
    0: "Lewandowski",
    1: "Swoboda",
    2: "Błachowicz",
    3: "Smolarek",
    4: "Małysz",
    5: "Kowalczyk"
}

FIFO_PATH = 'kolejka'

def create_fifo(fifo_path):
    try:
        os.mkfifo(fifo_path)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise

def request():
    time.sleep(5)
    create_fifo(FIFO_PATH)
    fifo = os.open(FIFO_PATH, os.O_RDONLY)
    requests_str = ""
    while True:
        r = os.read(fifo, 128)
        if len(r) > 0:
            requests_str += r.decode()
        else:
            print("Klient skończyl")
            break

    os.close(fifo)

    requests_array=[]
    for request in requests_str.strip().split("\n"):
        id, client = request.split(",")
        requests_array.append(( int(id), client))

    return requests_array

def main():
    while True:
        time.sleep(2)
        for id, client in request():
            data = database.get(id, "Not found")

            fifo = os.open(client, os.O_WRONLY)
            os.write(fifo, f"{data}\n".encode())
            os.close(fifo)

if __name__ == "__main__":
    main()