import os
import shutil
import platform
import subprocess


def register_custom_font(font_filename):
    # Теперь папка fonts лежит на уровень выше utils/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(base_dir, "fonts", font_filename)

    if not os.path.exists(font_path):
        print(f"Шрифт {font_filename} не найден в папке fonts/")
        return None

    user_font_dir = os.path.expanduser("~/.local/share/fonts")
    os.makedirs(user_font_dir, exist_ok=True)
    target_path = os.path.join(user_font_dir, font_filename)
    if not os.path.exists(target_path):
        shutil.copy(font_path, target_path)

    if platform.system() == "Linux":
        os.system("fc-cache -f > /dev/null 2>&1")
        try:
            result = subprocess.run(["fc-scan", "--format", "%{family}", target_path],
                                    capture_output=True, text=True)
            internal_name = result.stdout.strip()
            if internal_name:
                return internal_name
        except Exception as e:
            print(f"Ошибка при получении имени шрифта: {e}")

    return os.path.splitext(font_filename)[0]