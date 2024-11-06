import requests
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO

def get_image(url_api):
    answer = requests.get(url_api)
    image = BytesIO(answer.content)
    img = Image.open(image)
    img_tk = ImageTk.PhotoImage(img)
    return img_tk


url = "https://cataas.com/cat"

window =Tk()

label = Label(window)
label.pack()

get_image(url)

window.mainloop()