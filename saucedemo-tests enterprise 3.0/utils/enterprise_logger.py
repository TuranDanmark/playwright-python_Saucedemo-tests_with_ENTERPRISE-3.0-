import allure
from functools import wraps


def enterprise_step(title: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            msg = title.format(*args, **kwargs)
            print(f"\n📌 STEP :: {msg}")

            with allure.step(msg):
                return func(*args, **kwargs)

        return wrapper
    return decorator
