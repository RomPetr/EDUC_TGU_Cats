import requests
from tkinter import *
from PIL import Image, ImageTk

def get_image(url_api):
    answer = requests.get(url_api)
    print(answer)


url = "https://cataas.com/cat"

window =Tk()

label = Label(window)
label.pack()

get_image(url)

window.mainloop()