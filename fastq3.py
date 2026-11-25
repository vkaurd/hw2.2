import os
from tkinter import filedialog, messagebox
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# 1.ПРОЕКТ

class Reader:

    def __init__(self, filename):
        self.filename = filename


class SequenceReader(Reader):

    def validate_sequence(self, sequence): #проверка ошибок: смотрим, чтобы в ДНК были только буквы A, T, G, C
        sequence = sequence.upper() # перевод строки в большие буквы
        for letter in sequence:
            if letter not in ["A", "T", "G", "C", "N"]:
                return False # если нашли не ту букву — ошибка
        return True

    def get_sequences_count(self): #Считаем, сколько всего штук ДНК в файле
        if not os.path.exists(self.filename): #файла нет — ошибка
            return 0
        count = 0
        for item in self.read(): # перебираем всё, что выдало
            count = count + 1 # нашли 1 ДНК — прибавили 1
        return count

    def get_average_length(self): #считаем среднюю длину ДНК в файле
        if not os.path.exists(self.filename):
            return 0
        total_length = 0
        count = 0
        for item in self.read():
            dna_string = item[1] # строка с ДНК идет второй в результате
            total_length = total_length + len(dna_string) 
            # считаем длину этой строки и прибавляем к общей сумме
            count = count + 1
        if count == 0: # если файл пустой, чтобы не делить на ноль
            return 0
        return total_length / count # делим общую длину на количество штук


class FastqReader(SequenceReader):

    def read(self): #читаем файлы FASTQ блоками по 4 строки
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r") as f:
            while True:
                line1 = f.readline()
                line2 = f.readline()
                line3 = f.readline()
                line4 = f.readline()

                # если первая строка пустая, значит файл закончился, выходим из цикла
                if line1 == "":
                    break
                # проверка ошибок: если файл оборвался на середине блока
                if line2 == "" or line3 == "" or line4 == "":
                    print("Ошибка: Файл сломан, в нем не хватает строк!")
                    break

                name = line1.strip()[1:] # имя (убираем '@')
                dna = line2.strip() # буквы ДНК
                quality = line4.strip() # значки качества
                # Проверка ошибок:
                if self.validate_sequence(dna) == False:
                    print("Внимание! В FASTQ нашли другие буквы!")
                if len(dna) != len(quality):
                    print("Ошибка: Кол-во букв и значков качества не совпадает!")
                yield name, dna, quality

# 2. ГРАФИЧЕСКИЙ ИНТЕРФЕЙС

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# открываем обычное окно проводника с фильтром только на FASTQ
def choose_fastq_file():
    file_path = filedialog.askopenfilename(
        title="Выберите файл формата FASTQ",
        filetypes=[("FASTQ файлы", "*.fastq *.fq")],
    )
    # если окно выбора закрыли без выбора файла
    if not file_path:
        return

    # запускаем парсер
    reader = FastqReader(file_path)
    total_reads = reader.get_sequences_count() #считаем общее кол-во последовательностей
    avg_len = reader.get_average_length() #средн длина

    if total_reads == 0:
        messagebox.showerror(
            "Ошибка", "Файл пустой или не соответствует формату FASTQ!"
        )
        return

    # пишем имя файла и базовую статистику
    file_name = os.path.basename(file_path) #убирает папки слева, оставляя только имя
    info_label.configure(
        text=f"Файл: {file_name}  |  Записей ДНК: {total_reads}  |  Средняя длина: {round(avg_len, 1)}"
    ) #меняем текст на плашке в верх часте окна

    # считаем качество и количество букв A, T, G, C
    all_positions = {} #словарь для 1 графика: ключ — № позиции буквы, значение — список всех оценок качества на этой позиции.
    letters_count = {"A": 0, "T": 0, "G": 0, "C": 0, "N": 0} #2 граф
    for name, dna, quality_string in reader.read():
        for n in dna.upper():
            if n in letters_count:
                letters_count[n] += 1

        for i in range(len(quality_string)):
            score = ord(quality_string[i]) - 33
            if i not in all_positions:
                all_positions[i] = [] #создаем новый пустой список, когда встречаем эту позицию
            all_positions[i].append(score)

    x_points = sorted(all_positions.keys())
    y_points = []
    for pos in x_points:
        scores = all_positions[pos]  # берем список всех оценок для этой позиции
        avg = sum(scores) / len(scores)  # считаем среднюю оценку
        y_points.append(avg)  # добавляем её в список точек для графика

    # очищаем старые графики перед выводом новых
    for widget in charts_frame.winfo_children():
        widget.destroy()

    # создаем два графика рядом
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    #лист, оси. 1 строка 2 столбца, ширина высота.
    fig.subplots_adjust(wspace=0.3)
    #ширина между граф 30% от ширины

    # 1. график качества по позициям
    axes[0].plot(x_points, y_points, color="#1f6aa5", linewidth=2)
    axes[0].set_title("Среднее качество по позициям")
    axes[0].set_xlabel("Позиция нуклеотида")
    axes[0].set_ylabel("Качество (Phred)")

    # 2. график количества нуклеотидов, диаграмма bar
    axes[1].bar(
        list(letters_count.keys()),
        list(letters_count.values()),
        color=["#50b88e", "#e26a8d", "#f5a623", "#4a90e2", "gray"],
    )
    axes[1].set_title("Распределение нуклеотидов")
    axes[1].set_xlabel("Нуклеотид")
    axes[1].set_ylabel("Количество")

    # встраиваем графики прямо в окно
    canvas = FigureCanvasTkAgg(fig, master=charts_frame)#лист с графиками привязываем к ниж рамке
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

#ГЛАВНОЕ ОКНО
window = ctk.CTk()
window.title("FastQ")
window.geometry("980x620")

top_panel = ctk.CTkFrame(window) #плашка
top_panel.pack(fill="x", padx=15, pady=15)

# кнопка выбора FASTQ файла
select_btn = ctk.CTkButton(
    top_panel,
    text="Выбрать FASTQ файл...",
    font=("Arial", 14, "bold"),
    height=40,
    command=choose_fastq_file,
)
select_btn.pack(side="left", padx=15, pady=12)
info_label = ctk.CTkLabel(
    top_panel,
    text="Нажмите кнопку, чтобы открыть файл",
    font=("Arial", 14),
) #инфа справа от кнопки
info_label.pack(side="left", padx=15)

charts_frame = ctk.CTkFrame(window) # рамка для графиков
charts_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

window.mainloop()
