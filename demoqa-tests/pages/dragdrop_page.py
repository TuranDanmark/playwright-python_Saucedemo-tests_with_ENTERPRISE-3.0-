import logging
from .base_page import BasePage
from playwright.sync_api import expect

class DragDropPage(BasePage):
    def __init__(self, page):
        super().__init__(page, "https://demoqa.com/droppable")
        self.drag = page.locator("#draggable")
        self.drop = page.locator("div#simpleDropContainer #droppable")

    def drag_and_drop(self):
        logging.info("Начинаю операцию drag & drop.")
        self.drag.drag_to(self.drop)
        expect(self.drop).to_contain_text("Dropped!")
        logging.info("Drag & drop выполнен успешно.")
