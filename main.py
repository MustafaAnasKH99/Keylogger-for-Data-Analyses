import pynput
from pynput.keyboard import Key, Listener

def on_press(e):
    print('{0} pressed '.format(e))

def on_release(e):
    if e == Key.esc:
        return False

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()