import math
import customtkinter as ctk

# включаем темную тему
ctk.set_appearance_mode("dark")

window = ctk.CTk() #создаем само главное окно программы.
window.title("Калькулятор")
window.geometry("320x450")

# поле ввода сверху
entry = ctk.CTkEntry(window, font=("Arial", 26), justify="right", height=60)
#где лежит, шрифт, выравнивание текста, высота окошка 
entry.pack(fill="x", padx=15, pady=15)
# приклеить окошко к окну, растянуть на всю ширину. окошко с отступом на 15 пикс по ох и оу

# --- ФУНКЦИИ ---
# дописывает символ на экран
def write_symbol(symbol):
    if "Ошибка" in entry.get(): #убираем старую ошибку с экрана
        entry.delete(0, "end") #стереть текст с 0 символа до конца
    entry.insert("end", symbol)#новый символ в конец


# очищает весь экран (кнопка C)
def clear_all():
    entry.delete(0, "end")


# удаляет один последний символ (кнопка <-)
def delete_last():
    text = entry.get()
    entry.delete(0, "end")
    entry.insert(0, text[:-1])


# считает квадратный корень (кнопка sqrt)
def get_sqrt():
    try:
        number = float(entry.get())
        if number < 0:
            clear_all()
            entry.insert(0, "Ошибка: корень < 0")
            return
        result = math.sqrt(number)
        clear_all()
        entry.insert(0, str(round(result, 4))) #округл до 4 знаков
    except Exception:
        clear_all()
        entry.insert(0, "Ошибка ввода")

# считает пример (кнопка = или клавиша Enter)
def calculate(event=None): #чтобы ф-ция работала от мыши и клавиатуой
    text = entry.get()
    try:
        # проверяем в цикле, что нет лишних букв
        for n in text:
            if n not in "0123456789+-*/.":
                clear_all()
                entry.insert(0, "Ошибка: лишние буквы")
                return
        result = eval(text) #счет примера
        clear_all()
        entry.insert(0, str(round(result, 4)))
    except ZeroDivisionError:
        clear_all()
        entry.insert(0, "Ошибка: деление на 0")
    except Exception: #другие случаи
        clear_all()
        entry.insert(0, "Ошибка ввода")


# ф-ция кнопок
def make_button_action(symbol):
    def action():
        write_symbol(symbol)
    return action

# привязываем клавишу Enter к функции подсчета
window.bind("<Return>", calculate) #return = enter в системе, запуск ф-ции calculate

# --- СОЗДАНИЕ СЕТКИ КНОПОК ---
panel = ctk.CTkFrame(window, fg_color="transparent") #создаем невидимый контейнер для кнопок, прозрачн цвет
panel.pack(fill="both", expand=True, padx=15, pady=(0, 15)) 
#панель растягиваем по высоте и ширине, на все свободн место, 
#делаем отступы 15 слева и справа, 0 сверх, 15 сниз

# циклом делаем все 5 строк и 4 столбца одинаковыми по размеру
for i in range(5): # горизонт кнопки от 0 до 4
    panel.grid_rowconfigure(i, weight=1) # строки и столбцы растяг одинаково
for j in range(4): # вертикальные 
    panel.grid_columnconfigure(j, weight=1)

# таблица кнопок: (текст_на_кнопке, строка, столбец, цвет). кортеж
buttons = [
    ("C", 0, 0, "red"),
    ("<-", 0, 1, "gray"),
    ("sqrt", 0, 2, "orange"),
    ("/", 0, 3, "orange"),
    ("7", 1, 0, "#333333"),
    ("8", 1, 1, "#333333"),
    ("9", 1, 2, "#333333"),
    ("*", 1, 3, "orange"),
    ("4", 2, 0, "#333333"),
    ("5", 2, 1, "#333333"),
    ("6", 2, 2, "#333333"),
    ("-", 2, 3, "orange"),
    ("1", 3, 0, "#333333"),
    ("2", 3, 1, "#333333"),
    ("3", 3, 2, "#333333"),
    ("+", 3, 3, "orange"),
    ("0", 4, 0, "#333333"),
    (".", 4, 1, "#333333"),
    ("=", 4, 2, "green"),
]

# проходим циклом по списку и создаем каждую кнопку
for text, row, col, color in buttons:
    if text == "C":
        b1 = clear_all
    elif text == "<-":
        b1 = delete_last
    elif text == "sqrt":
        b1 = get_sqrt
    elif text == "=":
        b1 = calculate
    else:
        b1 = make_button_action(text)

    # кнопка '=' columnspan занимает сразу 2 столбца остальные по 1
    if text == "=":
        width = 2
    else:
        width = 1

    btn = ctk.CTkButton(panel, text=text, font=("Arial", 20), fg_color=color, command=b1)
    #создвем саму кнопку внутри панели
    btn.grid(row=row, column=col, columnspan=width, sticky="nsew", padx=3, pady=3)
    #ставим кнопку на нужное место в сетке, sticky - крепим кнопку ко всем 4 краям, щели по 3 пикс


# запуск окна
window.mainloop()
