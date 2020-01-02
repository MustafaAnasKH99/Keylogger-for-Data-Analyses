# For Beginner - Analyse your own daily activity by building a Python keylogger

A while ago, I was curious to know more about my own activity on the web. I tried installing my browser search history and do some analysis on that but I didnt like the result considering the effort done to analyze such big data. I wanted to keep it simple. So I thought why not start by capturing every single word my keyboard types and see what I can conclude from there.

So in This tutorial I will show you how to build a keylogger in Python that will allow us to store the words we type in a `.txt` file then we can see how to analyse/represent this data (It should be fun 😉).

> FIRST THINGS FIRST 🎆 . I am close to my first 1000 followers on Dev even though I have not been super active yet. So I want to thank everyone who has been following me (I am glad you like my writings) and promise better engagement from now on 😄.

Great, lets get to it.

## Simple Python - Save and Write keys pressed 🦄

This wont be any complicated. To do this we will only need two functions:
 - One that stores each key pressed in an array.
 - One that takes the keys stored in the array and write them in a `.txt` file.

Lets define the first function calling it `on_press`:

```python
keys = []
def on_press(e):
    global keys  #access the array keys
    keys.append(e)  #add the key e to the array
```
This function takes an argument which will be the key pressed (we will pass it in a bit), then access the global keys array, then add the key pressed to that array. But so far out function does not run as we did not call it yet. So we need to call this function everytime a key is pressed. To do that we will import few modules from the `pynput` library.
at the very top of your `.py` file, lets add this line:

```python
from pynput.keyboard import Key, Listener
```

and at the very bottom of the file, lets use the Listener library we imported to call the function we just defined (`on_press`) everytime a key is pressed.

```python
with Listener(on_press = on_press) as listener:
    listener.join()
```

Great. Now our code looks like this:

```python
from pynput.keyboard import Key, Listener

keys = []
def on_press(e):
    global keys  #access the array keys
    keys.append(e)  #add the key e to the array

with Listener(on_press = on_press) as listener:
    listener.join()    
```

If we run it, we wont be seeing anything but the code will be recording the logs in the `keys` array.
Next step is to take these keys and output them into a `.txt` file.
Lets define our second function (`that takes the keys stored in the array and write them in a `.txt` file.`).

```python
def write_file(keys):
    with open("log.txt", "a+") as f: #the a+ tells python to create log.txt if it does not exist
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                    f.write('  ')
            elif k.find("Key") == -1:
                    f.write(k)
```

Great. Now this function opens the `log.txt` file, goes throw the array we have, then write the key to the file (`as f`). However, we have few conditionals here. first we remove any `'` key, then if the key pressed is `"space"`, we dont want to write the word space so instead we will just type an actual space `" "` in a string. Otherwise, we just type the key as it is.

Great 🔥 Now we have the function ready, but when do we call it??
As you saw, there are two steps to the `.txt` file. First storing the keys in an array, second taking the keys from the array and typing them to a file. _WHICH MEANS_, we have to call the functiobn `write_file` only after we store the key in the array. However, since the `write_file` function goes through the array one by one, we cannot call it everytime we add a key to the array since it will type it again and again. So lets only call it everytime there are 10 keys in the array, and after we call it, we make that array empty again.

So lets edit the `on_press` function:

```python
count = 0 # his keeps track of how many items there are in the array
keys = []

def on_press(e):
    global keys, count
    keys.append(e)
    count += 1
    if count >= 10:
        count = 0
        write_file(keys)
        keys = []  # make the array empty after we call the write_file function.
```

Looks like we did it!
Our final code looks like this:

```python
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
    with open("log.txt", "a+") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                    f.write('  ')
            elif k.find("Key") == -1:
                    f.write(k)

with Listener(on_press = on_press) as listener:
    listener.join()
```

yayy 🦄
Now run this code, try typing some sentences anywhere, they force close the code.
You will see a new `log.txt` file appear in the same directory your code is in. You will see the keys nicely formated as words in one line. 
Now the next step is to read these words and try to analyze them.