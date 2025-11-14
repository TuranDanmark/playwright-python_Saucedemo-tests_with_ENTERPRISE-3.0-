import allure
import datetime
import json
import os
import traceback
from functools import wraps
from colorama import Fore, Style, init

# Инициализация цветного вывода
init(autoreset=True)

# Папка логов
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "test.log")
JSON_LOG_FILE = os.path.join(LOG_DIR, "steps.json")


def _timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _write_text_log(message: str):
    """Запись шагов в текстовый log-файл."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{_timestamp()}] {message}\n")


def _write_json_log(step: dict):
    """Запись шагов в JSON-файл."""
    with open(JSON_LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(step, f, ensure_ascii=False)
        f.write("\n")


def _console_log(message: str):
    """Цветной и красивый вывод в консоль."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.CYAN}[{timestamp}] {Fore.YELLOW}ШАГ: {Fore.GREEN}{message}{Style.RESET_ALL}")


def allure_step(step_name):
    """
    ENTERPRISE-декоратор:
    ✔ шаги в Allure
    ✔ цветной лог в консоль
    ✔ запись в текстовый лог-файл
    ✔ запись в JSON
    ✔ авто-скриншот при ошибке (если есть self.page)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            step_data = {
                "timestamp": _timestamp(),
                "step": step_name,
                "function": func.__name__,
                "args": str(args[1:]),
                "kwargs": kwargs,
            }

            _console_log(step_name)
            _write_text_log(f"STEP: {step_name}")
            _write_json_log(step_data)

            with allure.step(step_name):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    # Пытаемся снять скриншот если внутри PageObject
                    instance = args[0]
                    page = getattr(instance, "page", None)

                    if page:
                        screenshot_path = f"logs/{func.__name__}_error.png"
                        page.screenshot(path=screenshot_path)
                        allure.attach.file(
                            screenshot_path,
                            name=f"{step_name} (screenshot)",
                            attachment_type=allure.attachment_type.PNG
                        )
                        print(Fore.RED + f"[ERROR] Скриншот сохранён: {screenshot_path}")

                    # лог ошибки
                    error_message = f"ERROR in STEP '{step_name}': {e}"
                    _write_text_log(error_message)

                    traceback.print_exc()

                    raise e

        return wrapper
    return decorator
