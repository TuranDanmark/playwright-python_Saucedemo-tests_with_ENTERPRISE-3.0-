import logging
from .base_page import BasePage

class AlertsPage(BasePage):
    def __init__(self, page):
        super().__init__(page, "https://demoqa.com/alerts")
        self.alert_button = page.locator("#alertButton")
        self.timer_button = page.locator("#timerAlertButton")

    def trigger_alert(self):
        logging.info("Вызываю обычное окно alert().")
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.alert_button.click()
        logging.info("Alert успешно принят.")

    def trigger_timer_alert(self):
        logging.info("Вызываю alert с таймером.")
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.timer_button.click()
        self.page.wait_for_timeout(6000)
        logging.info("Alert с таймером успешно принят.")
