from tkinter import *
from decimal import Decimal
import math

# Цветовая палитра
BG_COLOR = "#1C1C1E"  # Темный фон
BTN_BG_COLOR = "#2C2C2E"  # Фон кнопок
BTN_ACTIVE_COLOR = "#3A3A3C"  # Фон кнопок при нажатии
BTN_TEXT_COLOR = "#FFFFFF"  # Цвет текста кнопок
ACCENT_COLOR = "#FF9500"  # Цвет кнопок операций и "="
RESULT_COLOR = "#000000"  # Цвет текста результата
RESULT_BG_COLOR = "#FFFFFF"  # Фон области результата

root = Tk()
root.title('Advanced Calculator')
root.configure(bg=BG_COLOR)
root.geometry("375x600")

active_str = ''
stack = []

# Функция для вычислений
def calculate():
    global stack
    if len(stack) < 3:
        return
    try:
        operand2 = Decimal(stack.pop())
        operation = stack.pop()
        operand1 = Decimal(stack.pop())

        if operation == '+':
            result = operand1 + operand2
        elif operation == '-':
            result = operand1 - operand2
        elif operation == '/':
            if operand2 == 0:
                raise ZeroDivisionError
            result = operand1 / operand2
        elif operation == '*':
            result = operand1 * operand2
        elif operation == '%':
            result = operand1 * operand2 / 100
        else:
            result = 0

        stack.append(str(result))
        label.configure(text=str(result))
    except ZeroDivisionError:
        stack.clear()
        label.configure(text='Неопределено')

# Функция для выполнения операций с одним операндом
def single_operation(op):
    global active_str
    global stack
    try:
        if active_str:
            operand = Decimal(active_str)
        else:
            operand = Decimal(label['text'])

        if op == 'x²':
            result = operand ** 2
        elif op == '√':
            if operand < 0:
                raise ValueError
            result = math.sqrt(operand)
        elif op == '1/x':
            if operand == 0:
                raise ZeroDivisionError
            result = 1 / operand
        else:
            result = operand

        label.configure(text=str(result))
        active_str = str(result)
    except ZeroDivisionError:
        label.configure(text='Неопределено')
        active_str = ''
    except ValueError:
        label.configure(text='Ошибка')
        active_str = ''

# Функция для обработки нажатий кнопок
def click(text):
    global active_str
    global stack
    if text == 'CE':
        stack.clear()
        active_str = ''
        label.configure(text='0')
    elif '0' <= text <= '9':
        active_str += text
        label.configure(text=active_str)
    elif text == '.':
        if '.' not in active_str:
            active_str += text
            label.configure(text=active_str)
    elif text in ('+', '-', '*', '/', '%'):
        if active_str:
            stack.append(active_str)
            active_str = ''
        if len(stack) == 2:
            stack.append(text)
            calculate()
        else:
            stack.append(text)
        label.configure(text=text)
    elif text == '=':
        if active_str:
            stack.append(active_str)
            active_str = ''
        if len(stack) == 3:
            calculate()

# Обработчик событий клавиатуры
def key_press(event):
    key = event.char
    if key in '0123456789.+-*/=':
        click(key)
    elif key == '\r':  # Enter key
        click('=')
    elif key == '\x08':  # Backspace
        global active_str
        active_str = active_str[:-1]
        label.configure(text=active_str or '0')

# Создание метки для отображения ввода и результата
label = Label(root, text='0', font=('Arial', 30), bg=RESULT_BG_COLOR, fg=RESULT_COLOR, anchor='e', padx=10)
label.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(10, 0))

# Кнопка "CE" рядом с результатом
Button(root, text='CE', font=('Arial', 18), bg='#FF3B30', fg=BTN_TEXT_COLOR, activebackground='#FF6666',
       command=lambda: click('CE')).grid(row=0, column=4, sticky="nsew", padx=(0, 10), pady=(10, 0))

# Кнопки калькулятора
buttons = [
    ('%', '√', 'x²', '1/x'),
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', '.', '=', '+')
]

for row, row_values in enumerate(buttons):
    for col, text in enumerate(row_values):
        if text in ('%', '√', 'x²', '1/x'):
            cmd = lambda t=text: single_operation(t)
        else:
            cmd = lambda t=text: click(t)
        Button(root, text=text, font=('Arial', 18), bg=BTN_BG_COLOR, fg=BTN_TEXT_COLOR,
               activebackground=BTN_ACTIVE_COLOR, command=cmd).grid(
            row=row + 1, column=col, sticky="nsew", padx=5, pady=5)

# Настройка строк и столбцов для равномерного распределения
for i in range(len(buttons) + 1):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

root.grid_columnconfigure(4, weight=0)

# Привязка обработчика клавиатуры
root.bind('<Key>', key_press)

root.mainloop()
