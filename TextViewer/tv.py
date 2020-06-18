from tkinter import *
from tkinter import ttk, font, filedialog
from TextViewer import textfile
import os

class TV(object):
    # 可选编码
    CODEC = ["ascii", "gbk", "utf-8", "gb2312", "utf-16"]
    # 可选(文字，背景)颜色
    COLORS = {"白色": ("#000000", "#ffffff"),
              "护眼绿": ("#000000", "#cce8cf"),
              "深蓝": ("#fff6e6", "#415062")}

    def __init__(self):
        self.text = None
        self.cur_color = "护眼绿"
        self.cur_codec = 0
        self.font_size = 15
        self.if_chapter = False

        self.root = Tk()
        self.construct()
        self.root.mainloop()

    def construct(self):
        """
        构建如下格局
        --------------------------------
        章   |       具体内容
        节   |
        列   |
        表   |
        信   |
        息   |
        --------------------------------
        章节   打开文件  背景颜色 + - 编码
        --------------------------------
        """
        # 基本窗口
        self.root.title("Text查看器")
        self.root.geometry('800x600')
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
        self.chapter_button = ttk.Button(status_frame, text="章节", command=self.show_chapter, state="disabled", takefocus=0)
        self.chapter_button.grid(column=0, row=0, sticky=W)
        self.openfile_button = ttk.Button(status_frame, text="打开文件", command=self.open_file, takefocus=0)
        self.openfile_button.grid(column=1, row=0, sticky=(E,W))
        self.percent_label = ttk.Label(status_frame, text="0 %")
        self.percent_label.grid(column=2, row=0, sticky=E)
        self.color_box = ttk.Combobox(status_frame, values=list(TV.COLORS.keys()), state="readonly", takefocus=0)
        self.color_box.set(self.cur_color)
        self.color_box.bind('<<ComboboxSelected>>', self.change_color)
        self.color_box.grid(column=3, row=0, sticky=E)
        self.bigger_button = ttk.Button(status_frame, text="+", command=self.bigger_font, state="disabled", takefocus=0)
        self.bigger_button.grid(column=4, row=0, sticky=E)
        self.smaller_button = ttk.Button(status_frame, text="-", command=self.smaller_font, state="disabled", takefocus=0)
        self.smaller_button.grid(column=5, row=0, sticky=E)
        self.codec_box = ttk.Combobox(status_frame, values=TV.CODEC, state="readonly", takefocus=0)
        self.codec_box.current(self.cur_codec)
        self.codec_box.bind('<<ComboboxSelected>>', self.change_codec)
        self.codec_box.grid(column=6, row=0, sticky=E)
        
    def key_bind(self):
        """
        快捷键：
        空格——翻页
        """
        self.root.bind("<space>", self.next_page)

    def destroy(self):
        """
        打开新文件之前的恢复工作
        """
        self.root.title("Text查看器")
        self.content_text.destroy()
        self.chapters_lb.destroy()
        self.content_scroll.destroy()
        self.chapter_scroll.destroy()

    def show_content_widgets(self):
        """
        选择新文件/修改编码后调用
        显示具体的章节及内容信息，设置按钮及快捷键
        """
        # 具体内容
        self.content_text = Text(self.content_frame, padx=30, 
            font=font.Font(size=self.font_size), 
            background=TV.COLORS[self.cur_color][1], foreground=TV.COLORS[self.cur_color][0])
        self.content_text.grid(column=0, row=0, sticky=(N, W, E, S)) 
        self.content_text.insert("1.0", self.text.get_content())
        self.content_text.configure(state="disabled")
        # 滚动条
        self.content_scroll = ttk.Scrollbar(self.content_frame, orient=VERTICAL, command=self.content_text.yview)
        self.content_scroll.grid(column=1, row=0, sticky=(N, S))
        #self.content_text.configure(yscrollcommand=self.content_scroll.set)
        self.content_text.configure(yscrollcommand=self.change_view)

        # 章节信息
        v = StringVar()
        v.set(self.text.get_chapters())

        self.chapters_lb = Listbox(self.chapter_frame, listvariable=v, background="#cccccc")
        self.chapters_lb.grid(column=0, row=0, sticky=(N, W, E, S))
        self.chapters_lb.bind('<<ListboxSelect>>', self.select_chapter)
        # 滚动条
        self.chapter_scroll = ttk.Scrollbar(self.chapter_frame, orient=VERTICAL, command=self.chapters_lb.yview)
        self.chapter_scroll.grid(column=1, row=0, sticky=(N, S))
        self.chapters_lb.configure(yscrollcommand=self.chapter_scroll.set)

        # 是否显示章节
        if not self.if_chapter:
            self.chapter_frame.grid_forget()

        # 使按钮有效
        self.chapter_button.configure(state="normal")
        self.color_box.configure(state="readonly")
        self.bigger_button.configure(state="normal")
        self.smaller_button.configure(state="normal")     

        self.key_bind()

# 下面都是回调函数
    def change_view(self, *num):
        self.content_scroll.set(num[0], num[1])
        percent = "{:.2f}".format(float(num[1])*100) + " %"
        self.percent_label.configure(text=percent)

    def open_file(self, *args):
        """
        “打开文件”按钮的回调函数
        打开TXT格式文件，设置窗口名称
        """
        filename = filedialog.askopenfilename(title='选择文件', 
            filetypes=[('TEXT', '*.txt'), ('All Files', '*')],
            initialdir=(os.path.expanduser('C:/')))
        if not filename:
            return
        elif self.text:
            self.destroy()
        # 设置窗口名称为小说路径
        self.root.title(filename)
        self.text = textfile.TextFile(filename, TV.CODEC[self.cur_codec])

        self.show_content_widgets()

    def next_page(self, *args):
        """
        空格键的回调函数
        翻页
        """
        self.content_text.yview_scroll(1, 'pages')

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
        if self.text:
            self.text.update_content(TV.CODEC[self.cur_codec])

            self.content_text.destroy()
            self.show_content_widgets()