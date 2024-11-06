import os
import errno
import time
import sys
import signal

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

    request_tuple=[]
    for request in requests_str.strip().split("\n"):
        id, client_path = request.split(",")
        request_tuple.append(( int(id), client_path))

    return request_tuple

def ignore_signal(signum, frame):
    pass


def handle_sigusr1(signum, frame):
    os.remove(FIFO_PATH)
    sys.exit(0)


def main():
    # print("PID:", os.getpid())
    while True:
        time.sleep(2)
        for id, client in request():
            data = database.get(id, "Nie ma")
            client_fifo = os.open(client, os.O_WRONLY)
            os.write(client_fifo, f"{data}\n".encode())
            os.close(client_fifo)

if __name__ == "__main__":
    signal.signal(signal.SIGHUP, ignore_signal)
    signal.signal(signal.SIGTERM, ignore_signal)
    signal.signal(signal.SIGUSR1, handle_sigusr1)
    main()