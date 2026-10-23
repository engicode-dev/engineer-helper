import tkinter as tk
from tkinter import ttk, messagebox
from utils.loaders import load_materials
from core import styles


def build_ui(parent, app_data):  # <-- Обязательно app_data
    parent.configure(bg=styles.COLORS["light"])
    db = load_materials()

    if not db:
        styles.create_label(parent, "Ошибка загрузки базы материалов.", fg_key="danger").pack(pady=50)
        return

    styles.create_label(parent, "1. Выберите категорию:", "subtitle").pack(pady=5)
    category_var = tk.StringVar(value=list(db.keys())[0])
    category_combo = styles.create_combobox(parent, textvariable=category_var, values=list(db.keys()))
    category_combo.pack(pady=5)

    styles.create_label(parent, "2. Выберите материал:", "subtitle").pack(pady=5)
    material_var = tk.StringVar()
    material_combo = styles.create_combobox(parent, textvariable=material_var)
    material_combo.pack(pady=5)

    def update_materials(event=None):
        category = category_var.get()
        materials_list = list(db[category].keys())
        material_combo['values'] = materials_list
        material_var.set(materials_list[0])

    category_combo.bind("<<ComboboxSelected>>", update_materials)
    update_materials()

    styles.create_label(parent, "Введите объем детали (в см³):", "subtitle").pack(pady=10)
    volume_var = tk.StringVar()
    volume_entry = styles.create_entry(parent, textvariable=volume_var)
    volume_entry.pack(pady=5)

    result_label = styles.create_label(parent, "", "result", "primary")
    result_label.pack(pady=10)

    def calculate_weight(*args):
        try:
            if not volume_var.get():
                result_label.config(text="")
                return
            volume_cm3 = float(volume_var.get())
            category = category_var.get()
            material = material_var.get()
            density_kg_m3 = db[category][material]
            mass_kg = (volume_cm3 * density_kg_m3) / 1_000_000
            result_label.config(text=f"Масса детали: {mass_kg:.3f} кг\n({mass_kg * 1000:.1f} г)")
        except ValueError:
            result_label.config(text="Ошибка: Введите число")
        except KeyError:
            result_label.config(text="Ошибка: Материал не найден")

    volume_var.trace_add("write", calculate_weight)
    material_var.trace_add("write", calculate_weight)

    def check_for_new_volume():
        if app_data.last_volume_cm3 is not None:
            new_val = f"{app_data.last_volume_cm3:.2f}"
            volume_var.set(new_val)
            app_data.last_volume_cm3 = None
        parent.after(500, check_for_new_volume)

    check_for_new_volume()