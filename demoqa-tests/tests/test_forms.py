import logging
from pages.form_page import FormPage
from playwright.sync_api import expect

def test_fill_form(page):
    logging.info("=== Тест формы начат ===")
    form = FormPage(page)
    form.open()
    form.fill_form()
    expect(page.locator(".modal-content")).to_be_visible()
    logging.info("=== Тест формы завершён успешно ===")
