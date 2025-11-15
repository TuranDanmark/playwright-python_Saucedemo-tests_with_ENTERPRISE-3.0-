from playwright.sync_api import sync_playwright

class APIClient:
    from playwright.sync_api import sync_playwright

    class APIClient:
        def __init__(self):
            self.playwright = None
            self.request = None

        def start(self):
            self.playwright = sync_playwright().start()
            self.request = self.playwright.request.new_context()

        def stop(self):
            if self.request:
                self.request.dispose()
            if self.playwright:
                self.playwright.stop()

        def get(self, url, **kwargs):
            return self.request.get(url, **kwargs)

        def post(self, url, data=None, json=None, **kwargs):
            return self.request.post(url, data=data, json=json, **kwargs)

        def delete(self, url, **kwargs):
            return self.request.delete(url, **kwargs)
