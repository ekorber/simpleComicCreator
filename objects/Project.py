from objects.Page import Page


class Project:

    def __init__(self, page_width: int, page_height: int):
        self.pages = [Page()]
        self.page_width = page_width
        self.page_height = page_height

    def add_new_page(self):
        self.pages.append(Page())

    def delete_page(self, index: int):
        self.pages.pop(index)