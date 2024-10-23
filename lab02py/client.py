import os
import time
import errno

def isLockfileExsist():
    while True:
        try:
            fd = os.open("lockfile", os.O_CREAT | os.O_EXCL | os.O_RDWR)
            return fd
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            else:
                print("Serwer zajęty")
                time.sleep(1)

def writeMessage(buffer_filename, client_filename):
    with open(buffer_filename, "a") as sb:
        sb.write(client_filename + "\n")
        while True:
            user_input = input("Napisz wiadomość (Napisz 'esc', aby zakończyć): ")
            if user_input.lower() == "esc":
                break

            sb.write(user_input + "\n")

def readMessage(client_filename):
    while not os.path.exists(client_filename):
        print("Czekam na odpowiedź...")
        time.sleep(3)

    with open(client_filename, "r") as response_file:
        print("Odpowiedź od serwera: \n", response_file.read())


if __name__ == "__main__":
    client_filename = input("Podaj nazwę swojego pliku: ") + ".txt"
    server_filename = "server_buffer.txt"
    fd = isLockfileExsist()
    writeMessage(server_filename, client_filename)
    readMessage(client_filename)
    os.close(fd) 
    os.unlink("lockfile")  
    os.remove(client_filename)