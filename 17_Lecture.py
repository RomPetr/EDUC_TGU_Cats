import requests
from tkinter import *
from tkinter import ttk
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
    tag = i_tag.get()
    url = "https://cataas.com/cat"
    url_tag = f"https://cataas.com/cat/{tag}"
    img = get_image(url_tag if tag else url)

    if img:
        new_window = Toplevel()
        new_window.title("Картинка с котиком")
        new_window.geometry("550x500")
        l = Label(new_window, image=img)
        l.pack()
        l.image = img


def exit_win():
    window.destroy()


sp_tags = ["sleep", "orange", "black", "cute", "smile", "fat", "circle"]

window =Tk()
window.title("Главное окно")
window.geometry("300x100")

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

lab = Label(window, text="Выберите тэг: ")
lab.pack()

# i_tag = Entry(window, font=("Arial", 15))
# i_tag.pack()

i_tag = ttk.Combobox(window, values=sp_tags)
i_tag.pack()

window.mainloop()