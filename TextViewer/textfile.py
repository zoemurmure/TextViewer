import re

class TextFile(object):
    # 自动识别章节信息的正则表达式
    PATTERN = re.compile(r'^[0-9]+\.?\s\S*|^第?[0-9一二三四五六七八九十百千]+[章节部]\s\S*|^chapter\s*[0-9]+\s\S*', re.MULTILINE)

    def __init__(self, file, codec):
        self.file_name = file
        self.content = []
        self.chapters = []
        self.codec = codec

        self.update_content(codec)

    def update_content(self, codec):
        """
        根据提供的编码格式更新文本内容
        为增加可读性，在段落间添加了一个换行符
        """
        self.content = []
        self.codec = codec
        with open(self.file_name, "r", encoding=codec, errors="ignore") as f:
            try:
                for line in f:
                    self.content += [line]
            except UnicodeDecodeError:
                self.content = ["无法解析文件内容"]
                
            self.content = "\n".join(self.content)

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

