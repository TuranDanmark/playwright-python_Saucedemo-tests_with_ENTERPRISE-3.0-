from .base_page import BasePage
from playwright.sync_api import expect

class FramesPage(BasePage):
    def __init__(self, page):
        super().__init__(page, "https://demoqa.com/frames")
        self.frame1 = "frame1"
        self.frame2 = "frame2"

    def check_frames(self):
        frame1 = self.page.frame(name=self.frame1)
        frame2 = self.page.frame(name=self.frame2)
        expect(frame1.locator("#sampleHeading")).to_have_text("This is a sample page")
        expect(frame2.locator("#sampleHeading")).to_have_text("This is a sample page")
