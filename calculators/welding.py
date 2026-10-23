import tkinter as tk
from core import styles

def build_ui(parent):
    parent.configure(bg=styles.COLORS["light"])

    styles.create_label(parent, "Калькулятор сварного шва (угловой шов)", "subtitle").pack(pady=10)

    # Поля ввода
    input_frame = tk.Frame(parent, bg=styles.COLORS["light"])
    input_frame.pack(pady=10)

    styles.create_label(input_frame, "Катет шва (K), мм:", "normal").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_k = styles.create_entry(input_frame)
    entry_k.grid(row=0, column=1, padx=5, pady=5)

    styles.create_label(input_frame, "Длина шва (L), мм:", "normal").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_l = styles.create_entry(input_frame)
    entry_l.grid(row=1, column=1, padx=5, pady=5)

    styles.create_label(input_frame, "Плотность металла, кг/м³:", "normal").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    # По умолчанию сталь 7850
    entry_rho = styles.create_entry(input_frame)
    entry_rho.insert(0, "7850")
    entry_rho.grid(row=2, column=1, padx=5, pady=5)

    result_label = styles.create_label(parent, "", "result", "primary", justify="left")
    result_label.pack(pady=20)

    def calculate(*args):
        try:
            # Получаем данные
            k = float(entry_k.get())
            l = float(entry_l.get())
            rho = float(entry_rho.get())

            # 1. Площадь сечения шва (для углового шва с катетом K)
            # Площадь прямоугольного треугольника с катетами K, умноженная на коэффициент выпуклости (обычно 0.7)
            # Упрощенно: F = 0.5 * K^2 * 0.7 (для стандартного шва)
            # Но в ГОСТ 5264-80 площадь сечения углового шва F = 0.5 * K^2 + 0.7 * K (для K до 10)
            # Для простоты используем классическую формулу: F = 0.7 * K^2 / 2
            area_mm2 = 0.7 * (k ** 2) / 2

            # 2. Объем наплавленного металла
            # V = F * L (в мм³)
            volume_mm3 = area_mm2 * l

            # 3. Масса наплавленного металла
            # Переводим мм³ в м³ (1 м³ = 1 000 000 000 мм³)
            volume_m3 = volume_mm3 / 1_000_000_000
            mass_kg = volume_m3 * rho

            # 4. Расход электродов (с учетом коэффициента потерь, обычно 1.5-1.6)
            # Берем средний коэффициент 1.6
            electrode_mass_kg = mass_kg * 1.6

            result_text = (
                f"--- Результаты расчета ---\n"
                f"Катет шва (K): {k} мм\n"
                f"Длина шва (L): {l} мм\n\n"
                f"Площадь сечения шва: {area_mm2:.2f} мм²\n"
                f"Объем наплавленного металла: {volume_mm3:.2f} мм³\n"
                f"Масса наплавленного металла: {mass_kg:.4f} кг\n"
                f"Расход электродов (с коэф. 1.6): {electrode_mass_kg:.4f} кг"
            )
            result_label.config(text=result_text)

        except ValueError:
            result_label.config(text="Ошибка: Введите числа во все поля!")
        except Exception as e:
            result_label.config(text=f"Ошибка: {e}")

    # Автоматический пересчет при вводе
    # Мы не можем использовать trace_add для всех полей сразу, поэтому привяжем к нажатию Enter или к кнопке
    # Но для удобства сделаем кнопку
    calc_button = styles.create_button(parent, "Рассчитать сварной шов", calculate, "warning", "subtitle")
    calc_button.pack(pady=10)

    # Также добавим привязку к Enter
    parent.bind('<Return>', lambda event: calculate())