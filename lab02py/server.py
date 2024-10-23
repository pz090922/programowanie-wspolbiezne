import os
import time
import errno

def isLockfileExsist():
    while True:
        print("Czekam na klienta")
        try:
            lockfile_esists = os.path.isfile("lockfile")
            if lockfile_esists:
                return
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        time.sleep(2)
        
def readMessage(buffer_filename):
    with open(buffer_filename, "r") as sb:
                filename = sb.readline().strip()
                message = sb.read()
    os.remove(buffer_filename)
    return filename, message

def readAndWriteMessage(buffer_filename):
    while True:
        try:
            client_filename, client_message = readMessage(buffer_filename)
            print("Wiadomość klienta: \n" + client_message)
            response = input("Wprowadź odpowiedź: ")
            with open(client_filename, "w") as response_file:
                response_file.write(response)
            break  
        except FileNotFoundError:
            time.sleep(2)
        except PermissionError:
            time.sleep(2)
            continue
    time.sleep(2)
    

if __name__ == "__main__":
    while True:
        isLockfileExsist()
        readAndWriteMessage("server_buffer.txt")