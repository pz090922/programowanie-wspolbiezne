import os
import errno
import time
import sys

FIFO_PATH = 'kolejka'

def create_fifo(fifo_path):
    try:
        os.mkfifo(fifo_path)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise

def wait(path):
    while not os.path.exists(path):
        time.sleep(1)

def read_response(fifo):
    response = b""
    # zakonczenie nowa linia.
    while not response.endswith(b"\n"):
        response += os.read(fifo, 128)

    return response.decode()

def write_to_database(id, client_path):
    fifo = os.open(FIFO_PATH, os.O_WRONLY)
    os.write(fifo, f"{id},{client_path}\n".encode())
    os.close(fifo)

def read_from_database(client_path):
    fifo = os.open(client_path, os.O_RDONLY)
    data = read_response(fifo)
    os.close(fifo)
    return data

def main():
    client_path = input("Podaj ścieżke: ")
    create_fifo(client_path)
    id = input("ID: ")
    wait(FIFO_PATH)
    write_to_database(id, client_path)
    print("Wynik: ", read_from_database(client_path))
    os.remove(client_path)

if __name__ == "__main__":
    main()

