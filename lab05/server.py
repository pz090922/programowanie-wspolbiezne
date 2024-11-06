import sysv_ipc
import time

input_queue_key = 1234
output_queue_key = 5678

input_queue = sysv_ipc.MessageQueue(input_queue_key, sysv_ipc.IPC_CREAT)
output_queue = sysv_ipc.MessageQueue(output_queue_key, sysv_ipc.IPC_CREAT)

dict = {
    "pies": "dog",
    "piłka": "ball",
    "marchewka": "carrot"
}

print("Serwer czeka...")

while True:
    if input_queue.current_messages > 0:
        message, message_type = input_queue.receive()
        time.sleep(0.1)

        word = message.decode()

        translation = dict.get(word, "Nie ma")
        print(f"({message_type}) przetłumaczenie '{word}' na '{translation}'")

        output_queue.send(translation.encode(), type=message_type)