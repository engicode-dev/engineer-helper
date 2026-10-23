import tkinter as tk
from tkinter import ttk, messagebox
from utils.loaders import load_tolerances
from core import styles


def build_ui(parent):
    parent.configure(bg=styles.COLORS["light"])
    data = load_tolerances()
    intervals = data["intervals"]
    tolerances_um = data["tolerances_um"]

    def get_interval_index(d):
        for i, interval in enumerate(intervals):
            if d <= interval["max"]:
                return i
        return None

    def calculate():
        try:
            d = float(entry_d.get())
            idx = get_interval_index(d)
            if idx is None:
                messagebox.showerror("Ошибка", "Диаметр должен быть до 500 мм")
                return

            it_hole = hole_qual_var.get()
            it_shaft = shaft_qual_var.get()
            tol_hole = tolerances_um[it_hole][idx]
            tol_shaft = tolerances_um[it_shaft][idx]

            hole_ES = tol_hole; hole_EI = 0
            shaft_type = shaft_dev_var.get()

            if shaft_type == "h":
                shaft_es = 0; shaft_ei = -tol_shaft; precision_note = "(точный расчет)"
            elif shaft_type == "k":
                shaft_ei = 2 if d < 100 else 3; shaft_es = shaft_ei + tol_shaft; precision_note = "(приближенно!)"
            elif shaft_type == "g":
                shaft_es = -int(tol_shaft * 0.4); shaft_ei = shaft_es - tol_shaft; precision_note = "(приближенно!)"
            else:
                shaft_es = 0; shaft_ei = -tol_shaft; precision_note = ""

            hole_ES_mm = hole_ES / 1000; hole_EI_mm = hole_EI / 1000
            shaft_es_mm = shaft_es / 1000; shaft_ei_mm = shaft_ei / 1000
            max_gap = hole_ES_mm - shaft_ei_mm
            min_gap = hole_EI_mm - shaft_es_mm

            if min_gap >= 0:
                fit_type = "Посадка с зазором"
            elif max_gap <= 0:
                fit_type = "Посадка с натягом"
            else:
                fit_type = "Переходная посадка"

            result_text = (
                f"--- Допуски ---\n"
                f"Диаметр: {d} мм (интервал: {intervals[idx]['label']})\n"
                f"Отверстие {it_hole}: ES = +{hole_ES_mm:.3f} мм, EI = {hole_EI_mm:.3f} мм\n"
                f"Вал {shaft_type}{it_shaft} {precision_note}: es = {shaft_es_mm:.3f} мм, ei = {shaft_ei_mm:.3f} мм\n\n"
                f"--- Посадка ---\n"
                f"Максимальный зазор/натяг: {max_gap:.3f} мм\n"
                f"Минимальный зазор/натяг: {min_gap:.3f} мм\n"
                f"Тип: {fit_type}"
            )
            result_label.config(text=result_text)

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный диаметр!")

    # --- Интерфейс ---
    styles.create_label(parent, "Номинальный диаметр (мм):", "subtitle").pack(pady=5)
    entry_d = styles.create_entry(parent)
    entry_d.pack(pady=5)

    styles.create_label(parent, "Квалитет отверстия:", "subtitle").pack(pady=5)
    hole_qual_var = tk.StringVar(value="IT7")
    # Используем нашу новую функцию для Combobox
    hole_qual_combo = styles.create_combobox(parent, textvariable=hole_qual_var, values=list(tolerances_um.keys()))
    hole_qual_combo.pack(pady=5)

    styles.create_label(parent, "Отклонение вала:", "subtitle").pack(pady=5)
    shaft_dev_var = tk.StringVar(value="h")
    shaft_dev_combo = styles.create_combobox(parent, textvariable=shaft_dev_var, values=["h", "k", "g"])
    shaft_dev_combo.pack(pady=5)

    styles.create_label(parent, "Квалитет вала:", "subtitle").pack(pady=5)
    shaft_qual_var = tk.StringVar(value="IT6")
    shaft_qual_combo = styles.create_combobox(parent, textvariable=shaft_qual_var, values=list(tolerances_um.keys()))
    shaft_qual_combo.pack(pady=5)

    calc_button = styles.create_button(parent, "Рассчитать посадку", calculate, "info", "subtitle")
    calc_button.pack(pady=15)

    result_label = styles.create_label(parent, "", "result", "primary", justify="left")
    result_label.pack(pady=10)