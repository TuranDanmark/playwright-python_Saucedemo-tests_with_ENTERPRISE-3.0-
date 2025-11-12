from pages.dragdrop_page import DragDropPage

def test_drag_and_drop(page):
    dragdrop = DragDropPage(page)
    dragdrop.open()
    dragdrop.drag_and_drop()
