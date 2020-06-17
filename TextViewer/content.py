import re

class Content(object):
    colors = [("#000000", "#ffffff"), ("#000000", "#cce8cf"), ("#fff6e6", "#415062")]
    pattern = re.compile(r'第[0-9]+章\s+\S+')
    def __init__(self, file):
        self.file_name = file
        self.content = ""
        self.chapters = []
        self.font_size = 15
        self.if_chapter = True
        self.color_idx = 1

        self.set_content()
        self.set_chapters()

    def enable_chapter(self):
        self.if_chapter = True

    def disable_chapter(self):
        self.if_chapter = False

    def set_content(self):
        try:
            f = open(self.file_name, "r", encoding="utf-8")
            self.content = f.readlines()
        except UnicodeDecodeError:
            f = open(self.file_name, "r", encoding="gbk")
            self.content = f.readlines()
        finally:
            self.content = "\n".join(self.content)
            f.close()

    def set_chapters(self):
        self.chapters = Content.pattern.findall(self.content)

    def get_color(self):
        color = Content.colors[self.color_idx]
        self.color_idx = (self.color_idx + 1) % 3
        
        return color

    def increase_size(self):
        self.font_size += 1

    def decrease_size(self):
        self.font_size -= 1
