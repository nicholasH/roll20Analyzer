import os
from tkinter import filedialog
from tkinter import *

hightroll = [None, 0]
highestCritsus = [None, 0]
highestNats = [None, 0]
print([highestNats[0],highestCritsus[0],hightroll[0]])

if any(a is None for a in [highestNats[0],highestCritsus[0],hightroll[0]]):
    print(" worked")
else:
    print("didnt")