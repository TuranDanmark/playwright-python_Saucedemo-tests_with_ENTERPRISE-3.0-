import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Загружаем переменные окружения
load_dotenv(override=True)


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def credentials():
    return {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    }


@pytest.fixture(scope="function")
def page_with_video(tmp_path_factory, request):
    """
    Для каждого теста создаётся отдельный браузер и контекст.
    При падении делается скриншот и добавляется в HTML отчёт.
    """
    test_name = request.node.name
    video_dir = tmp_path_factory.mktemp(f"videos_{test_name}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir=str(video_dir))
        page = context.new_page()

        screenshots_dir = os.path.join("reports", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        yield page

        context.close()
        browser.close()


# --- добавляем хук для pytest-html ---
def pytest_configure(config):
    # создаём папку для скринов, если не существует
    os.makedirs("reports/screenshots", exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук pytest — выполняется после каждого теста.
    Если тест упал, создаёт скриншот и добавляет его в HTML отчёт.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page_with_video", None)
        if page:
            screenshot_path = os.path.join("reports", "screenshots", f"{item.name}.png")
            try:
                page.screenshot(path=screenshot_path)
                if "pytest_html" in item.config.pluginmanager.plugins:
                    extra = getattr(rep, "extra", [])
                    html_link = f'<div><a href="{screenshot_path}" target="_blank">📸 View Screenshot</a></div>'
                    extra.append(pytest_html.extras.html(html_link))
                    rep.extra = extra
                print(f"\n❌ Скриншот для '{item.name}' сохранён: {screenshot_path}")
            except Exception as e:
                print(f"⚠️ Ошибка при создании скриншота для {item.name}: {e}")
