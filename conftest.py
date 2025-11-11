import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Загружаем .env
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
def page_with_video():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="reports")
        page = context.new_page()
        yield page
        context.close()
        browser.close()
