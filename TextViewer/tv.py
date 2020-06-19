from tkinter import *
from tkinter import ttk, font, filedialog
#from textviewer import textfile
from icon import img
import textfile
import os, pickle, base64

class TV(object):
    # 可选编码
    CODEC = ["gbk", "utf-8", "ascii", "gb2312", "utf-16"]
    # 可选(文字，背景)颜色
    COLORS = {"白色": ("#000000", "#ffffff"),
              "护眼绿": ("#000000", "#cce8cf"),
              "深蓝": ("#fff6e6", "#415062")}

    def __init__(self, history_path, filename=""):
        self.text = None                # TextFile对象
        self.cur_color = "护眼绿"       # 当前背景颜色
        self.cur_codec = 0              # 当前编码索引 
        self.font_size = 15             # 默认字体大小 
        self.if_chapter = False         # 是否显示章节信息
        self.filename = filename        # 文本文件路径
        self.dumpfile = os.path.join(history_path, "history")      # 历史记录保存文件
        self.history_location = 0       # 第一次读取文本时的打开位置

        self.root = Tk()
        self.construct()
        self.key_bind()
        self.root.mainloop()

    def get_window_size(self):
        """
        窗口在非最大化时的默认大小
        此时数值约等于最大化
        """
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight() - 70

        return str(width)+"x"+str(height)+"+0+0"

    def construct(self):
        """
        构建如下格局
        -------------------------------------
        章   |       具体内容
        节   |
        列   |
        表   |
        信   |
        息   |
        -------------------------------------
        章节   打开文件 百分比 背景颜色 + - 编码
        -------------------------------------
        """
        # 基本窗口
        self.root.title("Text查看器")
        self.set_icon()
        self.root.geometry(self.get_window_size())
        self.root.state("zoomed") 
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)
        # 章节列表框架
        self.chapter_frame = ttk.Frame(self.root, padding="3")
        self.chapter_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.chapter_frame.rowconfigure(0, weight=1)
        # 具体内容框架
        self.content_frame = ttk.Frame(self.root, padding="3")
        self.content_frame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        # 设置栏
        status_frame = ttk.Frame(self.root, padding="3")
        status_frame.grid(column=0, columnspan=2, row=1, sticky=(N, W, E, S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=1)
        status_frame.columnconfigure(2, weight=1)
        status_frame.columnconfigure(3, weight=1)
        # 设置栏按钮
        self.chapter_button = ttk.Button(status_frame, text="章节", command=self.show_chapter)
        self.chapter_button.grid(column=0, row=0, sticky=W)
        self.openfile_button = ttk.Button(status_frame, text="打开文件", command=self.open_file, takefocus=0)
        self.openfile_button.grid(column=1, row=0, sticky=(E,W))
        self.percent_label = ttk.Label(status_frame, text="0 %")
        self.percent_label.grid(column=2, row=0, sticky=E)
        self.color_box = ttk.Combobox(status_frame, values=list(TV.COLORS.keys()), state="readonly")
        self.color_box.set(self.cur_color)
        self.color_box.bind('<<ComboboxSelected>>', self.change_color)
        self.color_box.grid(column=3, row=0, sticky=E)
        self.bigger_button = ttk.Button(status_frame, text="+", command=self.bigger_font)
        self.bigger_button.grid(column=4, row=0, sticky=E)
        self.smaller_button = ttk.Button(status_frame, text="-", command=self.smaller_font)
        self.smaller_button.grid(column=5, row=0, sticky=E)
        self.codec_box = ttk.Combobox(status_frame, values=TV.CODEC, state="readonly")
        self.codec_box.current(self.cur_codec)
        self.codec_box.bind('<<ComboboxSelected>>', self.change_codec)
        self.codec_box.grid(column=6, row=0, sticky=E)

        # 建立文本文件TextFile
        self.text = textfile.TextFile()
        # 显示文本内容的TEXT插件
        self.content_text = Text(self.content_frame, padx=30,spacing1=15, spacing2=10, spacing3=15,
            font=font.Font(size=self.font_size), 
            background=TV.COLORS[self.cur_color][1], foreground=TV.COLORS[self.cur_color][0])
        self.content_text.grid(column=0, row=0, sticky=(N, W, E, S)) 
        self.content_text.configure(state="disabled")
        # 滚动条
        self.content_scroll = ttk.Scrollbar(self.content_frame, orient=VERTICAL, command=self.content_text.yview)
        self.content_scroll.grid(column=1, row=0, sticky=(N, S))
        self.content_text.configure(yscrollcommand=self.change_view)
        # 章节信息
        self.chapters_lb = Listbox(self.chapter_frame, background="#cccccc")
        self.chapters_lb.grid(column=0, row=0, sticky=(N, W, E, S))
        self.chapters_lb.bind('<<ListboxSelect>>', self.select_chapter)
        # 滚动条
        self.chapter_scroll = ttk.Scrollbar(self.chapter_frame, orient=VERTICAL, command=self.chapters_lb.yview)
        self.chapter_scroll.grid(column=1, row=0, sticky=(N, S))
        self.chapters_lb.configure(yscrollcommand=self.chapter_scroll.set)

        # 是否显示章节
        if not self.if_chapter:
            self.chapter_frame.grid_forget()
        
        self.set_content()

    def set_icon(self):
        """
        设置窗口的icon图标
        """
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        self.root.iconbitmap("tmp.ico")
        os.remove("tmp.ico")

    def key_bind(self):
        """
        快捷键：
        空格 —— 下一页
        左右键 —— 翻页
        上下键 —— 上移或下移一行
        """
        self.root.bind_class("Text", "<space>", self.next_page)
        self.root.bind_class("Text", "<Right>", self.next_page)
        self.root.bind_class("Text", "<Left>", self.prev_page)
        self.root.bind_class("Text", "<Up>", self.prev_line)
        self.root.bind_class("Text", "<Down>", self.next_line)

    def set_content(self):
        """
        更新文本正文内容以及章节信息
        在打开软件、文件或者修改编码后调用
        """
        self.root.title("Text查看器 " + os.path.basename(self.filename))

        self.text.update_content(self.filename, TV.CODEC[self.cur_codec])

        self.content_text.configure(state="normal")
        self.content_text.delete("1.0", "end")
        self.content_text.insert("1.0", self.text.get_content())
        #self.content_text.pendingsync()
        #self.content_text.insert("1.0", os.getcwd())
        self.content_text.yview_moveto(self.history_location)
        self.content_text.configure(state="disabled")

        v = StringVar()
        v.set(self.text.get_chapters())
        self.chapters_lb.configure(listvariable=v)

    def save_history(self):
        """
        保存阅读历史
        在点击“打开文件”按钮或者关闭窗口时调用
        """
        # 检查文件是否存在
        try:
            f_read = open(self.dumpfile, "rb")
        except FileNotFoundError:
            f = open(self.dumpfile, "wb")
            f.close()
            f_read = open(self.dumpfile, "rb")
        # 检查文件是否为空
        try:
            history = pickle.load(f_read)
        except EOFError:
            history = {}
        finally:
            history[self.filename] = self.content_text.yview()[0]
        f_read.close()
        # 写入文件
        with open(self.dumpfile, "wb") as f_write:
            pickle.dump(history, f_write)

    def read_history(self):
        """
        获得阅读历史信息
        在打开文件之后调用
        """
        with open(self.dumpfile, "rb") as f_read:
            history = pickle.load(f_read)
            if self.filename in history.keys():
                self.history_location = history[self.filename]

    # 下面都是回调函数
    def close_window(self):
        """
        关闭按钮的回调函数
        保存阅读历史并关闭窗口
        """
        self.save_history()
        self.root.destroy()

    def change_view(self, *num):
        """
        内容TEXT的回调函数
        内容滚动时，修改滚动条位置及百分比数值
        """
        self.content_scroll.set(num[0], num[1])
        percent = "{:.2f}".format(float(num[1])*100) + " %"
        self.percent_label.configure(text=percent)

    def open_file(self, *args):
        """
        “打开文件”按钮的回调函数
        打开TXT格式文件，设置窗口名称
        """
        self.save_history()
        self.filename = filedialog.askopenfilename(title='选择文件', 
            filetypes=[('TEXT', '*.txt'), ('All Files', '*')],
            initialdir=(os.path.expanduser('C:/')))
        
        if not self.filename:
            return

        self.read_history()

        self.set_content()

    def prev_page(self, *args):
        """
        LEFT键的回调函数
        上一页
        """
        self.content_text.yview_scroll(-1, 'pages')

    def next_page(self, *args):
        """
        空格键、RIGHT键的回调函数
        翻页
        """
        self.content_text.yview_scroll(1, 'pages')

    def next_line(self, *args):
        """
        DOWN键的回调函数
        下一行
        """
        self.content_text.yview_scroll(1, 'units')

    def prev_line(self, *args):
        """
        UP键的回调函数
        上一行
        """
        self.content_text.yview_scroll(-1, 'units')

    def show_chapter(self, *args):
        """
        “章节”按钮的回调函数
        显示/隐藏章节信息
        """
        if self.if_chapter:
            self.if_chapter = False 
            self.chapter_frame.grid_forget()
        else:
            self.if_chapter = True
            self.chapter_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    def change_color(self, *args):
        """
        背景BOX的回调函数
        修改内容部分的背景及文字颜色
        共三种颜色可选：白、护眼绿、深蓝
        """
        self.cur_color = self.color_box.get()
        self.content_text.configure(background=TV.COLORS[self.cur_color][1])
        self.content_text.configure(foreground=TV.COLORS[self.cur_color][0])

    def bigger_font(self, *args):
        """
        “+”的回调函数
        增大字体
        """
        self.font_size += 1
        self.content_text.configure(font=font.Font(size=self.font_size))

    def smaller_font(self, *args):
        """
        “-”的回调函数
        减小字体
        """
        if self.font_size > 0:
            self.font_size -= 1
        self.content_text.configure(font=font.Font(size=self.font_size))

    def select_chapter(self, *args):
        """
        章节信息LISTBOX的回调函数
        跳转到选中章节
        """
        try:
            idx = int(self.chapters_lb.curselection()[0])
            self.content_text.yview(self.content_text.search(self.text.chapters[idx], 1.0))
        except IndexError:
            pass

    def change_codec(self, *args):
        """
        编码BOX的回调函数
        改变文本的编码格式
        """
        self.cur_codec = int(self.codec_box.current())
        self.save_history()
        self.set_content()
        self.read_history()