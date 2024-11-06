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
        img.thumbnail((550, 500))
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


def exit_win():
    window.destroy()


url = "https://cataas.com/cat"

window =Tk()
window.geometry("600x600")

label = Label(window)
label.pack()

# btn = Button(window, text="Получить котика", command=set_image)
# btn.pack(pady=10)

main_menu = Menu(window)
window.config(menu=main_menu)
file_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Файл", menu=file_menu)

file_menu.add_command(label="Получить котика", command=set_image)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=exit_win)

window.mainloop()