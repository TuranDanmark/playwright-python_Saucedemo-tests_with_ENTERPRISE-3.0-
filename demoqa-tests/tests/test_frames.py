from pages.frames_page import FramesPage

def test_frames(page):
    frames = FramesPage(page)
    frames.open()
    frames.check_frames()
