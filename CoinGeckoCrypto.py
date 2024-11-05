import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from PIL import Image, ImageTk
import requests
from io import BytesIO
import pprint

# Функция для получения списка криптовалют с сортировкой по рыночной капитализации
def get_crypto_market_data():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1
        })  # Получаем сразу 100 криптовалют
        response.raise_for_status()
        return response.json()
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")
        return None

# Функция для загрузки и отображения изображения криптовалюты
def update_crypto_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    image = image.resize((200, 200), Image.Resampling.LANCZOS)  # Изменяем размер изображения
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo  # Сохраняем ссылку на изображение для предотвращения его удаления


# Функция для получения и отображения курса, рыночной капитализации и изображения выбранной криптовалюты
def update_crypto_price_and_market_cap(event=None):
    selected_index = crypto_combobox.current()
    if selected_index != -1:
        crypto_id = crypto_combobox_ids[selected_index]
        market_cap = crypto_combobox_market_caps[selected_index]
        image_url = crypto_combobox_images[selected_index]
        price = get_crypto_price(crypto_id)

        price_label.config(text=f"Курс: ${price:.2f}")
        market_cap_label.config(text=f"Рыночная капитализация: ${market_cap:,.0f}")
        update_crypto_image(image_url)


# Функция для обновления списка криптовалют по выбранной группе
def update_crypto_list(event):
    print(group_combobox.get())
    group = int(group_combobox.get()) - 1

    start = group * 10
    end = start + 10
    crypto_names = [crypto["name"] for crypto in coins[start:end]]
    crypto_ids = [crypto["id"] for crypto in coins[start:end]]
    crypto_market_caps = [crypto["market_cap"] for crypto in coins[start:end]]
    crypto_images = [crypto["image"] for crypto in coins[start:end]]

    # Обновляем выпадающий список с криптовалютами и сохраняем данные
    crypto_combobox["values"] = crypto_names
    # crypto_combobox.current(0)
    crypto_combobox_ids.clear()
    crypto_combobox_ids.extend(crypto_ids)
    crypto_combobox_market_caps.clear()
    crypto_combobox_market_caps.extend(crypto_market_caps)
    crypto_combobox_images.clear()
    crypto_combobox_images.extend(crypto_images)

    # Устанавливаем первый элемент как выбранный, если список не пустой
    if crypto_names:
        crypto_combobox.current(0)
        # Обновляем цену, рыночную капитализацию и изображение для первой криптовалюты в группе
        update_crypto_price_and_market_cap()
    else:
        # Очищаем данные, если список пуст
        price_label.config(text="Курс: ")
        market_cap_label.config(text="Рыночная капитализация: ")
        image_label.config(image="")



# Функция для получения курса криптовалюты
def get_crypto_price(crypto_id):
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd")
        response.raise_for_status()
        price = response.json()
        return price[crypto_id]["usd"]
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка: {e}")
        return None

# Создаем интерфейс
root = tk.Tk()
root.title("Курс криптовалют")
root.geometry("350x370")

# Получаем список криптовалют
coins = get_crypto_market_data()
p = pprint.PrettyPrinter(indent=2)
p.pprint(coins)


crypto_combobox_ids = []
crypto_combobox_market_caps = []
crypto_combobox_images = []

# Выпадающий список для выбора группы
group_label = tk.Label(root, text="Выберите группу (1-10):")
group_label.pack()
group_combobox = ttk.Combobox(root, values=[str(i) for i in range(1, 11)], state="readonly")
group_combobox.current(0)
group_combobox.pack()
group_combobox.bind("<<ComboboxSelected>>", update_crypto_list)

# Выпадающий список для выбора криптовалюты
crypto_label = tk.Label(root, text="Выберите криптовалюту:")
crypto_label.pack()
crypto_combobox = ttk.Combobox(root, state="readonly")
crypto_combobox.pack()
crypto_combobox.bind("<<ComboboxSelected>>", update_crypto_price_and_market_cap)

# Метка для отображения курса
price_label = tk.Label(root, text="Курс: ")
price_label.pack(pady=10)

# Метка для отображения рыночной капитализации
market_cap_label = tk.Label(root, text="Рыночная капитализация: ")
market_cap_label.pack()

# Метка для отображения изображения криптовалюты
image_label = tk.Label(root)
image_label.pack(pady=10)

# Загрузка первой группы криптовалют
update_crypto_list(None)

# Запуск интерфейса
root.mainloop()

"""
Пояснения к обновленному коду:
1. crypto_images: при загрузке данных о криптовалютах теперь мы также сохраняем URL-адреса изображений каждой из них.
2. update_crypto_image: функция загружает изображение по URL и преобразует его для отображения в Tkinter с использованием PIL.
3. image_label: метка Label, предназначенная для отображения изображения криптовалюты. Мы устанавливаем изображение через config, а также сохраняем ссылку на него, чтобы предотвратить удаление изображения сборщиком мусора.

Эта версия программы будет корректно отображать как курс и рыночную капитализацию, так и изображение выбранной криптовалюты.
"""

"""
сделай в последнем листинге, где использовалась функция update_crypto_image исправления в функции "update_crypto_list" так как происходит ошибка при выборе группы криптовалют на строке crypto_combobox.current(0). 
Текст ошибки:
File "/usr/lib/python3.10/tkinter/ttk.py", line 712, in current
    return self.tk.call(self._w, "current", newindex)
_tkinter.TclError: Index 0 out of range

"""