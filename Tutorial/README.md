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

_To make sure you have pynput installed, run the command `pip install pynput`_

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

As I said before, I wanted to keep it simple. So all I did was to count:
 - How many characters
 - How many lines
 - How many words
 - how many times each word was repeated.

For the sake of keeping this simple and beginner-friendly, We will make a new python file that will do the reading/analysis work. So lets make a new `readKeys.py` file in the same directory and start working there.

Open `readKeys.py` and type the following:

```python
log_file = open("log.txt", "r+") #open file in reading mode (r)

chars = 0
lines = 0
letters = []

for i in log_file.read():
    if i == '\n':  # \n means Enter key which is a new line
        lines += 1
    chars += 1
    letters.append(i)
```

The loop we wrote reads the whole `log.txt` file that we got from the previouse code we wrote and counts how many characters and lines there are, and add the letters into an array. (we kind of re-did what we did in the previous code 😄).

Now what we want to do is to make a new array that has words and not letters.
The way we do this is by `joining` all the array letters into one string. Then we `split` this string to an array of words everytime we see a `space`
(_`split` and `join` are helpful methods that Python provide us. Lets see how easy it is to use them_).

```python
key_string = "".join(letters)
word_string = key_string.replace('\n', " ")
final_keywords_list = word_string.split()
```

This might look too complex but it is really not. Each line here does a step we mentioned before:
 - Join the letter in one string
 - replace the Enter spaces with proper spaces
 - split the string into an array of words

So now. The `final_keywords_list` is an array of words.
Now we can do the last bit of analysis. Lets count the repetative words!

First we define an empty dictionary called counted. Then we go through the array of words.
For each word, if it exists in the dictionary, we increase its count. If it does not, we add it.

```python
counted = {}

for letter in final_keywords_list:
    letr = str(letter)
    if letr in counted:
        counted[letr] += 1
    else:
        counted[letr] = 1
```

Sweet. Our code does what we want it to do so far. We have a dictionary that has each word typed and how many times it was repeated

## Lets get to visualization!

Since we have the words counted, why not do some filtering and data visualisation? The way we have the data know allows us to do many things (Sure, the more time you keep this code running, the more words you capture, and the more accurate your analysis can be).

For the sake of this tutorial, I chose to do a bar graph comparing repetative words.
For this we will use a library called `matplotlib`. It is the most famous library used in Data Science. So lets get to it. First make sure you install it. Instructions (here)[https://matplotlib.org/2.2.4/users/installing.html#linux].

So far, our code looks like this:

```python
log_file = open("log.txt", "r+")

chars = 0
lines = 0
letters = []
counted = {}

for i in log_file.read():
    if i == '\n':
        lines += 1
    chars += 1
    letters.append(i)

key_string = "".join(letters)
word_string = key_string.replace('\n', " ")
final_keywords_list = word_string.split()

for letter in final_keywords_list:
    letr = str(letter)
    if letr in counted:
        counted[letr] += 1
    else:
        counted[letr] = 1
```

Before we go ahead and draw a bar for each word in our dictionary, lets do some filtering.
If we run the code for a while, we will end up having A LOT of words captured. We wont really be able to draw a bar for every single word there is. So lets make a new dictionary containing the words that at least have been repeated 3 times.

```python
new_dict = {}  #making a new empty dictionary

for item in counted:  #looping through the old one
    if counted[str(item)] >= 3:  #if repeated more than 3 times
        new_dict[str(item)] = counted[str(item)]  #add to the new dictionary
``` 

## Amazing, now we can start drawing 🦄
First we need to import the library we installed:

```python
import matplotlib.pyplot as plt  #calling plt just makes it more convenient
```

Now at the bottom of our code, lets start plotting the words:

```python
plt.title('KEYLOG ANALYSIS', fontsize = 20)  #choosing a title for the graph
plt.bar(range(len(new_dict)), list(new_dict.values())) 
plt.xticks(range(len(new_dict)), list(new_dict.keys()))

plt.show()
```

Lets take a moment to explain that.
`plt.bar()` method takes many arguments. The default positional arguments are the x-coordinates of the graph (the words indexes), and the y-coordinates of the graph (the actual words).

`plt.xticks()` method is used to label the x-coordinates of the graph. So taking the keys of our dictionary as the second argument will plot each word beneath its bar.

Great. Now we are all set to try this out!
The final code looks like this:

```python
import matplotlib.pyplot as plt

log_file = open("log.txt", "r+")

chars = 0
lines = 0
letters = []
counted = {}
new_dict = {}

for i in log_file.read():
    if i == '\n':
        lines += 1
    chars += 1
    letters.append(i)

key_string = "".join(letters)
word_string = key_string.replace('\n', " ")
final_keywords_list = word_string.split()

for letter in final_keywords_list:
    letr = str(letter)
    if letr in counted:
        counted[letr] += 1
    else:
        counted[letr] = 1

for item in counted:
    if counted[str(item)] >= 3:
        new_dict[str(item)] = counted[str(item)]

print(lines, "Lines", " || ", chars, "Character", " || ", len(final_keywords_list), "Words")
print('\n')

plt.title('KEYLOG ANALYSIS', fontsize = 20)
plt.bar(range(len(new_dict)), list(new_dict.values()))
plt.xticks(range(len(new_dict)), list(new_dict.keys()))

plt.show()
```

Now the rest is for you to do. Just run the first keylogger we wrote. Do some work with your keyboard. Once you are done, run this code and see what it tells you!
Please feel free to share the result in a screenshot below (it can be really funny sometimes 😆).
Also, feel free to (clone the project on github)[https://github.com/MustafaAnasKH99/Daily-Activity-Analysis] and mess with it.

<a href="https://www.buymeacoffee.com/xERklFa" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>

> I am on a lifetime mission to support and contribute to the general knowledge of the web community as much as possible. Some of my writings might sound too silly, or too difficult, but no knowledge is ever useless.If you like my articles, feel free to help me keep writing by getting me coffee :wink: :heart:
