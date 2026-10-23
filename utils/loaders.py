import json
import os

def load_json(filename):
    """Универсальная загрузка JSON из папки data"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", filename)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден в папке data/")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка формата в {filename}")
        return {}

def load_materials():
    return load_json("materials.json")

def load_tolerances():
    return load_json("tolerances.json")