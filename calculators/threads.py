import tkinter as tk
from tkinter import ttk
from core import styles

# Справочник метрических резьб (ГОСТ 24705-2004)
# Формат: "M{номинал}": {"шаг": основной шаг, "d2": средний диаметр, "d1": внутренний диаметр}
THREADS = {
    "M2": {"шаг": 0.4, "d2": 1.740, "d1": 1.567},
    "M2.5": {"шаг": 0.45, "d2": 2.208, "d1": 2.013},
    "M3": {"шаг": 0.5, "d2": 2.675, "d1": 2.459},
    "M4": {"шаг": 0.7, "d2": 3.545, "d1": 3.242},
    "M5": {"шаг": 0.8, "d2": 4.480, "d1": 4.134},
    "M6": {"шаг": 1.0, "d2": 5.350, "d1": 4.918},
    "M8": {"шаг": 1.25, "d2": 7.188, "d1": 6.647},
    "M10": {"шаг": 1.5, "d2": 9.026, "d1": 8.376},
    "M12": {"шаг": 1.75, "d2": 10.863, "d1": 10.106},
    "M14": {"шаг": 2.0, "d2": 12.701, "d1": 11.835},
    "M16": {"шаг": 2.0, "d2": 14.701, "d1": 13.835},
    "M18": {"шаг": 2.5, "d2": 16.376, "d1": 15.294},
    "M20": {"шаг": 2.5, "d2": 18.376, "d1": 17.294},
}


def build_ui(parent):
    parent.configure(bg=styles.COLORS["light"])

    styles.create_label(parent, "Выберите номинальный диаметр резьбы:", "subtitle").pack(pady=10)

    thread_var = tk.StringVar(value="M10")
    thread_combo = styles.create_combobox(parent, textvariable=thread_var, values=list(THREADS.keys()))
    thread_combo.pack(pady=5)

    result_label = styles.create_label(parent, "", "result", "primary", justify="left")
    result_label.pack(pady=20)

    def calculate(*args):
        try:
            thread_name = thread_var.get()
            data = THREADS[thread_name]

            # Наружный диаметр (номинал) берем из имени (например, из "M10" получаем 10)
            nominal_d = float(thread_name[1:])

            text = (
                f"--- Резьба {thread_name} ---\n"
                f"Наружный диаметр (d): {nominal_d:.2f} мм\n"
                f"Средний диаметр (d2): {data['d2']:.3f} мм\n"
                f"Внутренний диаметр (d1): {data['d1']:.3f} мм\n"
                f"Шаг резьбы (P): {data['шаг']:.2f} мм\n\n"
                f"--- Полезные данные ---\n"
                f"Теоретическая высота профиля (H): {0.866 * data['шаг']:.3f} мм\n"
                f"Рабочая высота профиля (H1): {0.541 * data['шаг']:.3f} мм\n"
            )
            result_label.config(text=text)
        except Exception as e:
            result_label.config(text=f"Ошибка: {e}")

    # Автоматический пересчет при выборе
    thread_var.trace_add("write", calculate)
    calculate()  # Первый расчет при запуске