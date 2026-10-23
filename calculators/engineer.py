import tkinter as tk
from tkinter import messagebox
import math
from core import styles


def build_ui(parent):
    parent.configure(bg=styles.COLORS["light"]) # Задаем фон для фрейма

    expression = tk.StringVar()

    def add_to_display(char):
        current = expression.get()
        expression.set(current + str(char))

    def clear_display():
        expression.set("")

    def backspace():
        current = expression.get()
        expression.set(current[:-1])

    def calculate():
        try:
            current_expr = expression.get()
            open_brackets = current_expr.count("(")
            close_brackets = current_expr.count(")")
            if open_brackets > close_brackets:
                current_expr += ")" * (open_brackets - close_brackets)

            current_expr = current_expr.replace("×", "*").replace("÷", "/").replace("^", "**")
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            allowed_names["math"] = math

            result = eval(current_expr, {"__builtins__": None}, allowed_names)

            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            expression.set(str(result))

        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль!")
        except Exception:
            messagebox.showerror("Ошибка", "Неверное выражение!")

    # Дисплей (используем стандартный Entry, но с нужным шрифтом и фоном)
    display = tk.Entry(parent, textvariable=expression, font=(styles.BASE_FONT_FAMILY, 20), justify="right",
                       state="readonly", bd=5, relief="sunken", bg=styles.COLORS["white"])
    display.pack(fill="x", padx=10, pady=10)

    buttons_frame = tk.Frame(parent, bg=styles.COLORS["light"])
    buttons_frame.pack(padx=10, pady=10)

    buttons = [
        # ... (список кнопок остается прежним) ...
        ("sin", lambda: add_to_display("math.sin(math.radians(")),
        ("cos", lambda: add_to_display("math.cos(math.radians(")),
        ("tan", lambda: add_to_display("math.tan(math.radians(")),
        ("√", lambda: add_to_display("math.sqrt(")),
        ("C", clear_display), ("⌫", backspace),
        ("7", lambda: add_to_display("7")), ("8", lambda: add_to_display("8")), ("9", lambda: add_to_display("9")),
        ("÷", lambda: add_to_display("÷")), ("(", lambda: add_to_display("(")), (")", lambda: add_to_display(")")),
        ("4", lambda: add_to_display("4")), ("5", lambda: add_to_display("5")), ("6", lambda: add_to_display("6")),
        ("×", lambda: add_to_display("×")), ("^", lambda: add_to_display("^")),
        ("π", lambda: add_to_display("math.pi")),
        ("1", lambda: add_to_display("1")), ("2", lambda: add_to_display("2")), ("3", lambda: add_to_display("3")),
        ("-", lambda: add_to_display("-")), ("%", lambda: add_to_display("%")), ("e", lambda: add_to_display("math.e")),
        ("0", lambda: add_to_display("0")), (",", lambda: add_to_display(".")), ("=", calculate),
        ("+", lambda: add_to_display("+")),
    ]

    row_val = 0
    col_val = 0
    for (text, command) in buttons:
        # Используем разные цвета из палитры в зависимости от кнопки
        if text in ["=", "+"]:
            btn = styles.create_button(buttons_frame, text, command, "success", "normal", width=5, height=2)
        elif text in ["C", "⌫"]:
            btn = styles.create_button(buttons_frame, text, command, "danger", "normal", width=5, height=2)
        elif text in ["sin", "cos", "tan", "√", "π", "e"]:
            btn = styles.create_button(buttons_frame, text, command, "primary", "small", width=5, height=2)
        else:
            btn = styles.create_button(buttons_frame, text, command, "light", "normal", width=5, height=2)
            btn.config(fg="black") # Для светлых кнопок текст черный

        btn.grid(row=row_val, column=col_val, padx=2, pady=2)

        col_val += 1
        if col_val > 5:
            col_val = 0
            row_val += 1