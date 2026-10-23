import tkinter as tk
from tkinter import ttk, messagebox
import math
from core import styles


def build_ui(parent, app_data):
    parent.configure(bg=styles.COLORS["light"])

    shape_var = tk.StringVar(value="Цилиндр")

    styles.create_label(parent, "Выберите тип заготовки:", "subtitle").pack(pady=10)
    shape_combo = styles.create_combobox(parent, textvariable=shape_var, values=["Цилиндр", "Параллелепипед", "Труба"])
    shape_combo.pack(pady=5)

    input_frame = tk.Frame(parent, bg=styles.COLORS["light"])
    input_frame.pack(pady=10)

    # Поля (создаем с помощью styles.create_label, но нужно передать фон для Label)
    label_d = styles.create_label(input_frame, "Диаметр (D), мм:")
    entry_d = styles.create_entry(input_frame)
    label_h = styles.create_label(input_frame, "Высота/Длина (H), мм:")
    entry_h = styles.create_entry(input_frame)
    label_a = styles.create_label(input_frame, "Длина (A), мм:")
    entry_a = styles.create_entry(input_frame)
    label_b = styles.create_label(input_frame, "Ширина (B), мм:")
    entry_b = styles.create_entry(input_frame)
    label_c = styles.create_label(input_frame, "Высота (C), мм:")
    entry_c = styles.create_entry(input_frame)
    label_d_in = styles.create_label(input_frame, "Внутренний диаметр (d), мм:")
    entry_d_in = styles.create_entry(input_frame)

    def update_fields(event=None):
        for widget in [label_d, entry_d, label_h, entry_h, label_a, entry_a, label_b, entry_b, label_c, entry_c, label_d_in, entry_d_in]:
            widget.grid_forget()

        shape = shape_var.get()
        if shape == "Цилиндр":
            label_d.grid(row=0, column=0, sticky="e", padx=5, pady=5); entry_d.grid(row=0, column=1, padx=5, pady=5)
            label_h.grid(row=1, column=0, sticky="e", padx=5, pady=5); entry_h.grid(row=1, column=1, padx=5, pady=5)
        elif shape == "Параллелепипед":
            label_a.grid(row=0, column=0, sticky="e", padx=5, pady=5); entry_a.grid(row=0, column=1, padx=5, pady=5)
            label_b.grid(row=1, column=0, sticky="e", padx=5, pady=5); entry_b.grid(row=1, column=1, padx=5, pady=5)
            label_c.grid(row=2, column=0, sticky="e", padx=5, pady=5); entry_c.grid(row=2, column=1, padx=5, pady=5)
        elif shape == "Труба":
            label_d.grid(row=0, column=0, sticky="e", padx=5, pady=5); entry_d.grid(row=0, column=1, padx=5, pady=5)
            label_d_in.grid(row=1, column=0, sticky="e", padx=5, pady=5); entry_d_in.grid(row=1, column=1, padx=5, pady=5)
            label_h.grid(row=2, column=0, sticky="e", padx=5, pady=5); entry_h.grid(row=2, column=1, padx=5, pady=5)

    shape_combo.bind("<<ComboboxSelected>>", update_fields)
    update_fields()

    def calculate():
        try:
            shape = shape_var.get()
            volume_cm3 = 0.0
            area_cm2 = 0.0

            if shape == "Цилиндр":
                d_cm = float(entry_d.get()) / 10; h_cm = float(entry_h.get()) / 10; r = d_cm / 2
                volume_cm3 = math.pi * (r ** 2) * h_cm
                area_cm2 = 2 * math.pi * r * (r + h_cm)
            elif shape == "Параллелепипед":
                a_cm = float(entry_a.get()) / 10; b_cm = float(entry_b.get()) / 10; c_cm = float(entry_c.get()) / 10
                volume_cm3 = a_cm * b_cm * c_cm
                area_cm2 = 2 * (a_cm * b_cm + a_cm * c_cm + b_cm * c_cm)
            elif shape == "Труба":
                d_cm = float(entry_d.get()) / 10; d_in_cm = float(entry_d_in.get()) / 10; h_cm = float(entry_h.get()) / 10
                r_out = d_cm / 2; r_in = d_in_cm / 2
                volume_cm3 = math.pi * (r_out ** 2 - r_in ** 2) * h_cm
                area_cm2 = 2 * math.pi * (r_out * h_cm + r_in * h_cm + r_out ** 2 - r_in ** 2)

            result_label.config(text=f"Объем: {volume_cm3:.2f} см³\n"
                                     f"Площадь поверхности: {area_cm2:.2f} см²\n"
                                     f"({area_cm2 / 10000:.4f} м²)")
            app_data.last_volume_cm3 = volume_cm3

        except ValueError:
            result_label.config(text="Ошибка: Введите числа!")

    def send_to_weight():
        if app_data.last_volume_cm3 is not None:
            messagebox.showinfo("Успех", f"Объем {app_data.last_volume_cm3:.2f} см³ передан в калькулятор веса!")
        else:
            messagebox.showwarning("Внимание", "Сначала рассчитайте объем!")

    # Кнопки с новыми стилями
    calc_button = styles.create_button(parent, "Рассчитать объем и площадь", calculate, "success", "subtitle")
    calc_button.pack(pady=15)

    result_label = styles.create_label(parent, "", "result", "primary")
    result_label.pack(pady=10)

    send_button = styles.create_button(parent, "Передать объем в Вес ➡️", send_to_weight, "info", "normal")
    send_button.pack(pady=5)