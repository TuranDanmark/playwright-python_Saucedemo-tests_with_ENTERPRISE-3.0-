import allure
import datetime
import json
import os
import csv
import traceback
import time
from functools import wraps
from colorama import Fore, Style, init

init(autoreset=True)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

TEXT_LOG_FILE = os.path.join(LOG_DIR, "test.log")
JSON_LOG_FILE = os.path.join(LOG_DIR, "steps.json")
CSV_LOG_FILE = os.path.join(LOG_DIR, "steps.csv")
HAR_DIR = os.path.join(LOG_DIR, "har")
os.makedirs(HAR_DIR, exist_ok=True)

# Telegram (опционально)
TELEGRAM_ENABLED = False
TELEGRAM_TOKEN = ""
CHAT_ID = ""


def _timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _console(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.BLUE}[{timestamp}] {Fore.YELLOW}STEP: {Fore.GREEN}{msg}{Style.RESET_ALL}")


def _write_text(msg):
    with open(TEXT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{_timestamp()}] {msg}\n")


def _write_json(data):
    with open(JSON_LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")


def _write_csv(step, duration):
    write_header = not os.path.exists(CSV_LOG_FILE)
    with open(CSV_LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp", "step", "duration (ms)", "function", "args", "kwargs"])
        writer.writerow([
            _timestamp(),
            step,
            duration,
            step,
            "",
            ""
        ])


def _send_to_telegram(message):
    if not TELEGRAM_ENABLED:
        return
    import requests
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


def enterprise_step(step_name):
    """
    ENTERPRISE 2.0:
    ✔ Allure
    ✔ Console
    ✔ Text log
    ✔ JSON
    ✔ CSV
    ✔ Error screenshot
    ✔ HAR network log
    ✔ Telegram alert (optional)
    ✔ duration timing
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            _console(step_name)
            _write_text(f"STEP: {step_name}")

            step_json = {
                "timestamp": _timestamp(),
                "step": step_name,
                "function": func.__name__,
                "args": str(args[1:]),
                "kwargs": kwargs,
            }
            _write_json(step_json)

            with allure.step(step_name):
                try:
                    result = func(*args, **kwargs)

                    duration = int((time.time() - start_time) * 1000)
                    _write_csv(step_name, duration)

                    return result

                except Exception as e:
                    instance = args[0]
                    page = getattr(instance, "page", None)

                    # Screenshot
                    if page:
                        screenshot_path = f"logs/{func.__name__}_ERROR.png"
                        page.screenshot(path=screenshot_path)
                        allure.attach.file(
                            screenshot_path,
                            name=f"{step_name} ERROR screenshot",
                            attachment_type=allure.attachment_type.PNG
                        )

                    # HAR network capture
                    context = getattr(instance, "context", None)
                    if context:
                        har_file = os.path.join(HAR_DIR, f"{func.__name__}_error.har")
                        context.tracing.stop(path=har_file)
                        allure.attach.file(
                            har_file,
                            name=f"{step_name} HAR log",
                            attachment_type=allure.attachment_type.JSON
                        )

                    error_msg = f"ERROR in step '{step_name}': {str(e)}"
                    _write_text(error_msg)

                    _send_to_telegram(f"🔥 TEST FAILED\nStep: {step_name}\nError: {e}")

                    traceback.print_exc()
                    raise e

        return wrapper
    return decorator
