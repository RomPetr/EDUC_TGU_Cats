import requests
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import messagebox as mb

def get_image(url_api):
    try:
        answer = requests.get(url_api)
        image = BytesIO(answer.content)
        img = Image.open(image)
        img_tk = ImageTk.PhotoImage(img)
        return img_tk
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")
        return None


def set_image():
    img = get_image(url)

    if img:
        label.config(image=img)
        label.image = img


url = "https://cataas.com/cat"

window =Tk()

label = Label(window)
label.pack()

btn = Button(window, text="Получить котика", command=set_image)
btn.pack(pady=10)




window.mainloop()