import logging
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url

    def open(self):
        logging.info(f"Открываю страницу: {self.url}")
        self.page.goto(self.url)

    def check_title(self, title: str):
        logging.info(f"Проверяю, что заголовок страницы содержит: '{title}'")
        expect(self.page).to_have_title(title)
