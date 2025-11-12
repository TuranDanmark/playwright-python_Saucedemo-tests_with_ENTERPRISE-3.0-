import pytest
import os
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright

# -------------------
# Логирование
# -------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"test_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

logging.basicConfig(
    filename=log_file,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -------------------
# Playwright fixtures
# -------------------
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

# -------------------
# Screenshot on failure + HTML integration
# -------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)
        if page:
            reports_dir = "reports"
            os.makedirs(reports_dir, exist_ok=True)
            screenshot_path = os.path.join(reports_dir, f"{item.name}.png")
            page.screenshot(path=screenshot_path, full_page=True)
            if hasattr(report, "extra"):
                from pytest_html import extras
                report.extra.append(extras.image(screenshot_path))

# -------------------
# Metadata + dynamic naming
# -------------------
def pytest_configure(config):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = os.path.join("reports", f"report_{now}.html")

    config.option.htmlpath = report_file
    config.option.self_contained_html = True
    config._metadata = {
        "Project": "DemoQA Playwright",
        "Environment": "Local",
        "Tester": "Turan QA",
        "Browser": "Chromium"
    }
