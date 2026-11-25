import json  # сохранение и чтение файла
import os  # проверка наличия файла на диске
from tkinter import messagebox, ttk  # всплывающие окна ошибок и таблица
import customtkinter as ctk  # интерфейс
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # вставка графиков в окно
import matplotlib.pyplot as plt  # рисование графиков

# цветовая палитра: глубокий темно-синий и теплый бежевый
NAVY_BG = "#0f1c2e"  # фон главного окна
NAVY_PANEL = "#1a2d42"  # фон карточек и панелей
NAVY_ACCENT = "#2c4a6e"  # цвет кнопок и заголовков
BEIGE_LIGHT = "#f5efe6"  # светлый бежевый для текста и полей ввода
BEIGE_DARK = "#d9cbb8"  # теплый бежевый для рамок и акцентов
BEIGE_TEXT = "#1a2536"  # темный текст на бежевом фоне

ctk.set_appearance_mode("dark")  # базовый темный режим

DATA_FILE = "patients.json"  # имя файла для сохранения базы пациентов
patients = []  # главный список пациентов 
# расчет индекса массы тела
def calc_bmi(height_cm, weight_kg):
    height_m = height_cm / 100  
    return round(weight_kg / (height_m * height_m), 1)  # формула ИМТ с округлением до 1 знака


# сохранение списка пациентов в json-файл
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:  # открываем файл на запись
        json.dump(patients, file, ensure_ascii=False, indent=4)  # сохраняем с русскими буквами и отступами


# загрузка из файла при старте программы, если он уже был создан ранее
def load_data():
    global patients  # разрешаем изменять общий список
    if os.path.exists(DATA_FILE):  # проверяем, существует ли файл на диске
        with open(DATA_FILE, "r", encoding="utf-8") as file:  # открываем файл на чтение
            patients = json.load(file)  # загружаем данные в список


# проверка всех полей перед добавлением или редактированием
def check_form():
    surname = surname_entry.get().strip()  # берем фамилию без пробелов по краям
    first_name = name_entry.get().strip()  # берем имя без пробелов по краям
    patronymic = patronymic_entry.get().strip()  # берем отчество без пробелов по краям
    age_str = age_entry.get().strip()  # берем возраст
    gender = gender_box.get()  # берем выбранный пол
    height_str = height_entry.get().strip().replace(",", ".")  # берем рост и меняем запятую на точку
    weight_str = weight_entry.get().strip().replace(",", ".")  # берем вес и меняем запятую на точку

    # строка всех разрешенных русских букв и дефиса
    rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-"

    # проверка фамилии (обязательно, только русские буквы)
    if len(surname) < 2 or any(c not in rus for c in surname):
        messagebox.showerror("Ошибка", "Фамилия должна содержать только русские буквы!")
        return None

    # проверка имени (обязательно, только русские буквы)
    if len(first_name) < 2 or any(c not in rus for c in first_name):
        messagebox.showerror("Ошибка", "Имя должно содержать только русские буквы!")
        return None

    # проверка отчества (если имеется — проверяем, что там только русские буквы)
    if patronymic != "" and any(c not in rus for c in patronymic):
        messagebox.showerror("Ошибка", "Отчество должно содержать только русские буквы!")
        return None

    # проверка возраста (целое число от 0 до 120)
    if not age_str.isdigit() or not (0 <= int(age_str) <= 120):
        messagebox.showerror("Ошибка", "Возраст: целое число от 0 до 120 полных лет!")
        return None

    # проверка роста и веса
    try:
        height = float(height_str)  # превращаем текст роста в число
        weight = float(weight_str)  # превращаем текст веса в число
        if not (50 <= height <= 250):  # проверяем границы роста в см
            messagebox.showerror("Ошибка", "Рост указывается в см (от 50 до 250 см)!")
            return None
        if not (2 <= weight <= 300):  # проверяем границы веса в кг
            messagebox.showerror("Ошибка", "Вес указывается в кг (от 2 до 300 кг)!")
            return None
    except ValueError:  # если ввели буквы вместо цифр
        messagebox.showerror("Ошибка", "Рост (см) и вес (кг) должны быть числами!")
        return None

    # склеиваем полное ФИО для отображения в одном столбце таблицы
    full_name = f"{surname} {first_name} {patronymic}".strip()

    # возвращаем словарь с проверенными данными пациента
    return {
        "surname": surname,
        "first_name": first_name,
        "patronymic": patronymic,
        "full_name": full_name,
        "age": int(age_str),
        "gender": gender,
        "height": round(height, 1),
        "weight": round(weight, 1),
        "bmi": calc_bmi(height, weight),
    }


# обновление таблицы на экране
def refresh_table():
    for row in table.get_children():  # перебираем все старые строки таблицы
        table.delete(row)  # удаляем каждую старую строку

    for i, p in enumerate(patients):  # берем индекс i и словарь пациента p
        table.insert(  # вставляем новую строку в конец таблицы
            "",
            "end",
            iid=str(i),  # присваиваем строке номер, равный индексу в списке
            values=(p["full_name"], p["age"], p["gender"], p["height"], p["weight"], p["bmi"]),
        )


# очистка всех полей ввода слева
def clear_fields():
    surname_entry.delete(0, "end")  # очищаем поле фамилии
    name_entry.delete(0, "end")  # очищаем поле имени
    patronymic_entry.delete(0, "end")  # очищаем поле отчества
    age_entry.delete(0, "end")  # очищаем поле возраста
    height_entry.delete(0, "end")  # очищаем поле роста
    weight_entry.delete(0, "end")  # очищаем поле веса
    gender_box.set("Мужской")  # возвращаем пол по умолчанию
# добавление нового пациента
def add_patient():
    person = check_form()  # проверяем все поля ввода
    if person is not None:  # если ошибок нет
        patients.append(person)  # добавляем пациента в список
        save_data()  # сохраняем обновленный список в файл
        refresh_table()  # перерисовываем таблицу
        clear_fields()  # очищаем поля ввода


# подстановка данных выбранного пациента в поля слева при клике на строку
def select_row(event):
    selected = table.selection()  # получаем номер выбранной строки
    if not selected:  # если строка не выбрана
        return
    p = patients[int(selected[0])]  # находим пациента в списке по номеру строки
    clear_fields()  # очищаем поля перед заполнением
    surname_entry.insert(0, p["surname"])  # подставляем фамилию
    name_entry.insert(0, p["first_name"])  # подставляем имя
    patronymic_entry.insert(0, p["patronymic"])  # подставляем отчество
    age_entry.insert(0, str(p["age"]))  # подставляем возраст
    gender_box.set(p["gender"])  # выставляем пол в списке
    height_entry.insert(0, str(p["height"]))  # подставляем рост
    weight_entry.insert(0, str(p["weight"]))  # подставляем вес


# сохранение изменений выбранного пациента
def edit_patient():
    selected = table.selection()  # проверяем, выбрана ли строка
    if not selected:  # если строку не выбрали
        messagebox.showwarning("Внимание", "Сначала выберите пациента в таблице!")
        return
    person = check_form()  # проверяем новые данные из полей
    if person is not None:  # если ошибок нет
        patients[int(selected[0])] = person  # перезаписываем пациента в списке
        save_data()  # сохраняем изменения в файл
        refresh_table()  # обновляем таблицу
        clear_fields()  # очищаем поля ввода


# построение окна со сводной статистикой (4 графика)
def show_stats():
    if not patients:  # если таблица пустая
        messagebox.showwarning("Нет данных", "Таблица пуста! Добавьте хотя бы одного пациента.")
        return

    stats_win = ctk.CTkToplevel(window)  # создаем отдельное окно для графиков
    stats_win.title("Сводная статистика по пациентам")  # заголовок окна графиков
    stats_win.geometry("1020x740")  # размер окна графиков
    stats_win.configure(fg_color=NAVY_BG)  # темно-синий фон окна графиков

    fig, axes = plt.subplots(2, 2, figsize=(10, 7), facecolor=BEIGE_LIGHT)  # сетка 2x2 на бежевом фоне
    fig.subplots_adjust(hspace=0.42, wspace=0.3)  # отступы между графиками

    ages = [p["age"] for p in patients]  # список возрастов всех пациентов
    bmis = [p["bmi"] for p in patients]  # список ИМТ всех пациентов

    all_genders = ["Мужской", "Женский", "Другой"]  # все доступные полы
    gender_colors = {"Мужской": "#1f4e78", "Женский": "#c08552", "Другой": "#5c768d"}  # цвета для каждого пола

    present_genders = []  # полы, которые реально есть в таблице
    gender_counts = []  # количество людей каждого пола
    pie_colors = []  # цвета для присутствующих полов
    bmi_by_gender = []  # списки ИМТ отдельно по каждому полу

    for g in all_genders:  # перебираем каждый из 3 полов
        g_bmis = [p["bmi"] for p in patients if p["gender"] == g]  # берем ИМТ людей этого пола
        if len(g_bmis) > 0:  # если в таблице есть хотя бы один человек этого пола
            present_genders.append(g)  # добавляем название пола
            gender_counts.append(len(g_bmis))  # добавляем количество людей
            pie_colors.append(gender_colors[g])  # добавляем цвет
            bmi_by_gender.append(g_bmis)  # добавляем список ИМТ для графика

    # 1. круговая диаграмма распределения по полу (верхний левый график)
    axes[0, 0].pie(gender_counts, labels=present_genders, autopct="%1.1f%%", colors=pie_colors)
    axes[0, 0].set_title("1. Распределение по полу", color=BEIGE_TEXT, fontweight="bold")

    # 2. гистограмма распределения по возрасту (верхний правый график)
    axes[0, 1].set_facecolor(BEIGE_LIGHT)
    axes[0, 1].hist(ages, bins=8, color=NAVY_ACCENT, edgecolor=BEIGE_LIGHT)
    axes[0, 1].set_title("2. Распределение по возрасту", color=BEIGE_TEXT, fontweight="bold")
    axes[0, 1].set_xlabel("Возраст (полных лет)")
    axes[0, 1].set_ylabel("Количество (чел.)")

    # 3. ящик с усами ИМТ с учетом пола (нижний левый график)
    axes[1, 0].set_facecolor(BEIGE_LIGHT)
    axes[1, 0].boxplot(bmi_by_gender, tick_labels=present_genders)
    axes[1, 0].set_title("3. Распределение ИМТ с учетом пола", color=BEIGE_TEXT, fontweight="bold")
    axes[1, 0].set_ylabel("ИМТ (кг/м²)")

    # 4. точечный график зависимости ИМТ от возраста (нижний правый график)
    axes[1, 1].set_facecolor(BEIGE_LIGHT)
    axes[1, 1].scatter(ages, bmis, color="#8c5a2b", s=60, alpha=0.85)
    axes[1, 1].set_title("4. Зависимость ИМТ от возраста", color=BEIGE_TEXT, fontweight="bold")
    axes[1, 1].set_xlabel("Возраст (полных лет)")
    axes[1, 1].set_ylabel("ИМТ (кг/м²)")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    canvas = FigureCanvasTkAgg(fig, master=stats_win)  # связываем лист графиков с окном
    canvas.draw()  # отрисовываем графики
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)  # растягиваем на все окно


# --- ГЛАВНОЕ ОКНО ---
window = ctk.CTk()  # создаем главное окно
window.title("Учёт и статистика пациентов")  # заголовок окна
window.geometry("1020x760")  # размер окна
window.configure(fg_color=NAVY_BG)  # темно-синий фон окна

# левая карточка ввода данных
left_panel = ctk.CTkFrame(window, width=290, fg_color=NAVY_PANEL, border_width=1, border_color=BEIGE_DARK)
left_panel.pack(side="left", fill="y", padx=15, pady=15)  # прижимаем влево и растягиваем по высоте

ctk.CTkLabel(left_panel, text="Карточка пациента", font=("Arial", 17, "bold"), text_color=BEIGE_LIGHT).pack(pady=(12, 8))

# поле: фамилия
ctk.CTkLabel(left_panel, text="Фамилия (только русские буквы):", text_color=BEIGE_DARK, font=("Arial", 12)).pack(anchor="w", padx=15)
surname_entry = ctk.CTkEntry(left_panel, placeholder_text="Например: Иванов", fg_color=BEIGE_LIGHT, text_color=BEIGE_TEXT, width=260)
surname_entry.pack(pady=(0, 6), padx=15)

# поле: имя
ctk.CTkLabel(left_panel, text="Имя (только русские буквы):", text_color=BEIGE_DARK, font=("Arial", 12)).pack(anchor="w", padx=15)
name_entry = ctk.CTkEntry(left_panel, placeholder_text="Например: Иван", fg_color=BEIGE_LIGHT, text_color=BEIGE_TEXT, width=260)
name_entry.pack(pady=(0, 6), padx=15)

# поле: отчество
ctk.CTkLabel(left_panel, text="Отчество (если имеется, иначе -, рус. буквы):", text_color=BEIGE_DARK, font=("Arial", 12)).pack(anchor="w", padx=15)
patronymic_entry = ctk.CTkEntry(left_panel, placeholder_text="Например: Иванович", fg_color=BEIGE_LIGHT, text_color=BEIGE_TEXT, width=260)
patronymic_entry.pack(pady=(0, 6), padx=15)

# поле: возраст
ctk.CTkLabel(left_panel, text="Возраст (полных лет):", text_color=BEIGE_DARK, font=("Arial", 12)).pack(anchor="w", padx=15)
age_entry = ctk.CTkEntry(left_panel, placeholder_text="Например: 35", fg_color=BEIGE_LIGHT, text_color=BEIGE_TEXT, width=260)
age_entry.pack(pady=(0, 6), padx=15)

# поле: пол
ctk.CTkLabel(left_panel, text="Пол:", text_color=BEIGE_DARK, font=("Arial", 12)).pack(anchor="w", padx=15)
gender_box = ctk.CTkComboBox(
    left_panel,
    values=["Мужской", "Женский", "Другой"],  # список из 3 полов
    state="readonly",  # запрет ручного ввода текста с клавиатуры
    fg_color=BEIGE_LIGHT,
    text_color=BEIGE_TEXT,
    button_color=BEIGE_DARK,
    width=260,
)
gender_box.set("Мужской")  # значение по умолчанию
gender_box.pack(pady=(0, 6), padx=15)

# поле: рост
ctk.CTkLabel(left_panel, text="Рост (в сантиметрах, см):", text_color=BEIGE_DARK, font=("Arial", 12)).pack(anchor="w", padx=15)
height_entry = ctk.CTkEntry(left_panel, placeholder_text="Например: 175", fg_color=BEIGE_LIGHT, text_color=BEIGE_TEXT, width=260)
height_entry.pack(pady=(0, 6), padx=15)

# поле: вес
ctk.CTkLabel(left_panel, text="Вес (в килограммах, кг):", text_color=BEIGE_DARK, font=("Arial", 12)).pack(anchor="w", padx=15)
weight_entry = ctk.CTkEntry(left_panel, placeholder_text="Например: 70.5", fg_color=BEIGE_LIGHT, text_color=BEIGE_TEXT, width=260)
weight_entry.pack(pady=(0, 14), padx=15)

# кнопки управления в бежево-синей гамме
ctk.CTkButton(left_panel, text="Добавить пациента", fg_color=BEIGE_DARK, text_color=BEIGE_TEXT, hover_color=BEIGE_LIGHT, font=("Arial", 13, "bold"), command=add_patient, width=260).pack(pady=4, padx=15)
ctk.CTkButton(left_panel, text="Сохранить изменения", fg_color=NAVY_ACCENT, text_color=BEIGE_LIGHT, hover_color="#3a608f", command=edit_patient, width=260).pack(pady=4, padx=15)
ctk.CTkButton(left_panel, text="Очистить поля", fg_color="transparent", border_width=1, border_color=BEIGE_DARK, text_color=BEIGE_DARK, command=clear_fields, width=260).pack(pady=4, padx=15)
ctk.CTkButton(left_panel, text="Сводная статистика", fg_color="#8c5a2b", text_color=BEIGE_LIGHT, hover_color="#a66d37", height=38, font=("Arial", 13, "bold"), command=show_stats, width=260).pack(pady=(14, 10), padx=15)

# правая панель с таблицей
right_panel = ctk.CTkFrame(window, fg_color=NAVY_PANEL, border_width=1, border_color=BEIGE_DARK)
right_panel.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)  # занимает всё оставшееся место справа

# настройка цветов и шрифтов таблицы в бежево-синих тонах
style = ttk.Style()
style.theme_use("default")  # базовый стиль для возможности перекрашивания
style.configure("Treeview", background=BEIGE_LIGHT, foreground=BEIGE_TEXT, rowheight=28, fieldbackground=BEIGE_LIGHT, font=("Arial", 11))
style.configure("Treeview.Heading", background=NAVY_ACCENT, foreground=BEIGE_LIGHT, font=("Arial", 11, "bold"))
style.map("Treeview", background=[("selected", BEIGE_DARK)], foreground=[("selected", BEIGE_TEXT)])  # цвет выделенной строки

cols = ("full_name", "age", "gender", "height", "weight", "bmi")  # имена столбцов
table = ttk.Treeview(right_panel, columns=cols, show="headings")  # создаем таблицу без пустой колонки слева

# заголовки столбцов таблицы с единицами измерения
table.heading("full_name", text="ФИО")
table.heading("age", text="Возраст (лет)")
table.heading("gender", text="Пол")
table.heading("height", text="Рост (см)")
table.heading("weight", text="Вес (кг)")
table.heading("bmi", text="ИМТ (кг/м²)")

table.column("full_name", width=230)  # ширина столбца ФИО
for col in ("age", "gender", "height", "weight", "bmi"):  # настраиваем остальные столбцы
    table.column(col, width=85, anchor="center")  # ширина 85 и выравнивание по центру

table.pack(fill="both", expand=True, padx=12, pady=12)  # растягиваем таблицу на всю правую панель
table.bind("<<TreeviewSelect>>", select_row)  # привязываем клик по строке к функции select_row

load_data()
refresh_table()

# функция закрытия программы без фоновых предупреждений в терминале
def on_close():
    plt.close("all")  # закрываем все скрытые графики matplotlib в памяти
    window.quit()  # останавливаем главный цикл
    window.destroy()  # уничтожаем окно
window.protocol("WM_DELETE_WINDOW", on_close)  # привязываем крестик окна к нашей функции
window.mainloop()