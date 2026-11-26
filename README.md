# hw2.2
homework
# Графический интерфейс пользователя (GUI) на Python

Три учебных проекта с графическим интерфейсом на **CustomTkinter** и **Matplotlib**: калькулятор, база учёта пациентов и урезанный анализатор FASTQ-файлов.

## Быстрый старт (одна команда)

```bash
sudo apt update && sudo apt install git python3-tk python3-pil.imagetk python3-venv -y
git clone https://github.com
cd hw2.2
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install customtkinter matplotlib pillow
```

Проверка, что всё работает:

```bash
python3 calculator.py   # калькулятор
python3 patient.py      # учёт пациентов
python3 fastq3.py       # FastQ (выбрать файл)
```

---

## Проекты

### 1. Calculator (`calculator.py`)
Калькулятор с поддержкой базовых операций (`+`, `-`, `*`, `/`) и квадратного корня (`sqrt`). Поддерживает ввод как с экранной кнопочной панели, так и с физической клавиатуры (подсчёт по `=` или `Enter`), валидацию символов и обработку исключений (деление на ноль и корень из отрицательного числа).

**Запуск:**
```bash
python3 calculator.py
```

### 2. Форма учёта пациентов (`patient.py`)
Приложение для ведения базы пациентов:
* раздельный ввод ФИО;
* валидация данных на русском языке и контроль корректности возраста (лет), роста (см) и веса (кг);
* автоматический расчёт индекса массы тела (ИМТ);
* добавление, редактирование записей и автосохранение в `patients.json`;
* сводная статистика (4 графика `matplotlib`): распределение по полу (3 категории), возрасту, ИМТ с учётом пола и зависимость ИМТ от возраста.

**Запуск:**
```bash
python3 patient.py
```

### 3. FastQ (`fastq3.py`)
Графический интерфейс для модуля чтения последовательностей FASTQ:
* выбор файла через стандартный диалог проводника с фильтром форматов (`*.fastq`, `*.fq`);
* индикатор загрузки (`CTkProgressBar`) при обработке файла;
* вывод базовой статистики (число записей, средняя длина) и 2 графиков: качество нуклеотидов по позициям (Phred score) и состав нуклеотидов (`A, T, G, C, N`).

**Запуск:**
```bash
python3 fastq3.py
```

---

## Требования и установка зависимостей

* **Python 3.10** и новее (тестировалось на Python 3.12 в Ubuntu 24.04)
* Системные пакеты Linux: `python3-tk`, `python3-pil.imagetk`, `python3-venv`

Все Python-библиотеки собраны в `requirements.txt`:
```text
customtkinter
matplotlib
pillow
```

Установка вручную (после активации `venv`):
```bash
pip install customtkinter matplotlib pillow
```
