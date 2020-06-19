import re

class TextFile(object):
    # 自动识别章节信息的正则表达式
    PATTERN = re.compile(r'^\s*[0-9]+[\.、]?\s\S*|^\s*第?[0-9一二三四五六七八九十百千]+[章节部]\s\S*|^\s*chapter\s*[0-9]+\s\S*', re.MULTILINE)

    def __init__(self, file="", codec="utf-8"):
        self.filename = file
        self.content = "请选择打开的文件"
        self.chapters = []
        self.codec = codec

        #self.update_content(self.codec)

    def update_content(self, file="", codec="utf-8"):
        """
        根据提供的文件名和编码方式更新文本内容
        """
        if file=="" and self.filename == "":
            return
        elif file != "":
            self.filename = file

        self.codec = codec
        self.content = []
        with open(self.filename, "r", encoding=codec, errors="ignore") as f:
            try:
                for line in f:
                    self.content += [line]
            except UnicodeDecodeError:
                self.content = ["无法解析文件内容"]
                
            self.content = "".join(self.content)

        self.update_chapters()

    def update_chapters(self):
        """
        根据正则表达式自动识别文本中的章节名
        """
        self.chapters = TextFile.PATTERN.findall(self.content)

    def get_content(self):
        return self.content

    def get_chapters(self):
        return self.chapters

