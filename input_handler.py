import queue, time, threading
from pynput.keyboard import Key, Controller

input_queue = queue.Queue()

keyboard = Controller()

def press(key):
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)
    time.sleep(0.0001)          

def handle_inputs():
    while True:
        if not input_queue.empty():
            press(input_queue.get())

def init_thread():
    thread = threading.Thread(target=handle_inputs)
    thread.start()
    return thread