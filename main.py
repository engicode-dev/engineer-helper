import tkinter as tk
from core.app_data import AppData
from core import styles
from calculators import engineer, geometry, metal, tolerances, threads, welding


def open_calculator(title, build_func, app_data=None):
    window = tk.Toplevel()
    window.title(title)
    window.geometry("550x600")
    window.configure(bg=styles.COLORS["light"])

    frame = tk.Frame(window, bg=styles.COLORS["light"])
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    if app_data:
        build_func(frame, app_data)
    else:
        build_func(frame)


def main():
    root = tk.Tk()
    root.title("Инженерный Помощник")
    root.geometry("600x450")
    root.configure(bg=styles.COLORS["light"])

    app_data = AppData()

    title_label = tk.Label(root, text="Выберите инструмент", font=styles.FONTS["title"], bg=styles.COLORS["light"],
                           fg=styles.COLORS["dark"])
    title_label.pack(pady=20)

    buttons_frame = tk.Frame(root, bg=styles.COLORS["light"])
    buttons_frame.pack(pady=20)

    # --- Плитки меню (исправленные имена модулей) ---
    btn_eng = styles.create_menu_tile(buttons_frame, "🧮\nИнженерный\nкалькулятор",
                                      lambda: open_calculator("Инженерный калькулятор", engineer.build_ui),
                                      "primary")
    btn_eng.grid(row=0, column=0, padx=10, pady=10)

    btn_geom = styles.create_menu_tile(buttons_frame, "📐\nГеометрия\n(Объем/Площадь)",
                                       lambda: open_calculator("Геометрия", geometry.build_ui, app_data),
                                       "success")
    btn_geom.grid(row=0, column=1, padx=10, pady=10)

    btn_metal = styles.create_menu_tile(buttons_frame, "⚖️\nВес металла\nи материалов",
                                        lambda: open_calculator("Вес металла", metal.build_ui, app_data),
                                        "warning")
    btn_metal.grid(row=1, column=0, padx=10, pady=10)

    btn_tol = styles.create_menu_tile(buttons_frame, "📏\nДопуски\nи посадки",
                                      lambda: open_calculator("Допуски и посадки", tolerances.build_ui),
                                      "info")
    btn_tol.grid(row=1, column=1, padx=10, pady=10)

    btn_threads = styles.create_menu_tile(buttons_frame, "🔩\nРезьбы\n(Метрические)",
                                          lambda: open_calculator("Калькулятор резьб", threads.build_ui),
                                          "dark")  # Используем темный цвет для разнообразия
    btn_threads.grid(row=2, column=0, padx=10, pady=10)

    btn_weld = styles.create_menu_tile(buttons_frame, "🔥\nСварные\nшвы",
                                       lambda: open_calculator("Сварные швы", welding.build_ui),
                                       "danger")  # Используем красный цвет для сварки
    btn_weld.grid(row=2, column=1, padx=10, pady=10)

    footer = tk.Label(root, text="Инженерный Помощник v1.0", font=styles.FONTS["small"], bg=styles.COLORS["light"],
                      fg="gray")
    footer.pack(side="bottom", pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()