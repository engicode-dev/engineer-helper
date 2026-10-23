import tkinter as tk
from tkinter import ttk
from utils.font_manager import register_custom_font

GOST_FONT_NAME = register_custom_font("GOST_A.ttf")
# --- ЖЕСТКО ПРОПИСЫВАЕМ ИМЯ ШРИФТА ---
BASE_FONT_FAMILY = "GOSTRUS"


# --- Цветовая палитра ---
COLORS = {
    "primary": "#3498db", "success": "#2ecc71", "warning": "#e67e22",
    "danger": "#e74c3c", "info": "#9b59b6", "dark": "#2c3e50",
    "light": "#ecf0f1", "white": "#ffffff"
}

# --- Шрифты (теперь используют BASE_FONT_FAMILY) ---
FONTS = {
    "title": (BASE_FONT_FAMILY, 18, "bold"),
    "subtitle": (BASE_FONT_FAMILY, 14, "bold"),
    "normal": (BASE_FONT_FAMILY, 12),
    "small": (BASE_FONT_FAMILY, 10),
    "result": (BASE_FONT_FAMILY, 14, "bold")
}

# --- Функции для создания кнопок ---

def create_button(parent, text, command, color_key="primary", font_key="normal", **kwargs):
    """Универсальная функция для создания стилизованной кнопки"""
    return tk.Button(parent, text=text, command=command,
                     bg=COLORS[color_key], fg=COLORS["white"],
                     font=FONTS[font_key], padx=5, pady=3, **kwargs)

def create_menu_tile(parent, text, command, color_key):
    """Большая плитка для главного меню"""
    return tk.Button(parent, text=text, command=command,
                     bg=COLORS[color_key], fg=COLORS["white"],
                     font=(BASE_FONT_FAMILY, 14, "bold"), width=20, height=4,  # <-- ИСПРАВЛЕНО
                     bd=3, relief="raised")

def create_label(parent, text, font_key="normal", fg_key="dark", **kwargs):
    """Универсальная метка с нужным фоном"""
    return tk.Label(parent, text=text, font=FONTS[font_key],
                    bg=COLORS["light"], fg=COLORS[fg_key], **kwargs)


def create_entry(parent, textvariable=None):
    """Поле ввода с нужным шрифтом"""
    return tk.Entry(parent, textvariable=textvariable, font=FONTS["normal"])


def create_combobox(parent, textvariable=None, values=None):
    """Выпадающий список с нужным шрифтом (лечит баг с отображением выбранного элемента)"""
    style = ttk.Style()

    # Уникальное имя стиля
    style_name = "GOST.TCombobox"

    # Настраиваем шрифт для поля ввода
    style.configure(style_name, font=(BASE_FONT_FAMILY, 12))

    # ВАЖНО: Принудительно задаем цвет фона поля (в Linux это часто сбрасывает стандартный шрифт)
    style.map(style_name,
              fieldbackground=[("readonly", "white")],
              foreground=[("readonly", "black")])

    # Настраиваем шрифт для выпадающего списка (popup)
    parent.option_add('*TCombobox*Listbox.font', (BASE_FONT_FAMILY, 12))

    # Создаем сам Combobox
    combo = ttk.Combobox(parent, textvariable=textvariable, values=values,
                         state="readonly", style=style_name)

    # Дополнительный "костыль" для Linux: после создания принудительно ставим шрифт
    # через опцию font, если тема это позволяет
    combo.config(font=(BASE_FONT_FAMILY, 12))

    return combo