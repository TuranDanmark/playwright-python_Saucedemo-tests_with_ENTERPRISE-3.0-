from pages.alerts_page import AlertsPage

def test_alerts(page):
    alerts = AlertsPage(page)
    alerts.open()
    alerts.trigger_alert()
    alerts.trigger_timer_alert()
