from tkinter import *
from tkinter import ttk 
from tkinter import font
import windnd
from TextViewer import content

class TV(object):
    def __init__(self):
        self.text = None
        self.root = Tk()
        self.construct()
        self.root.mainloop()

    def construct(self):
        """
        -------------------------------
        章   |       具体内容
        节   |
        列   |
        表   |
        信   |
        息   |
        -------------------------------
        显示章节            背景颜色 + =
        -------------------------------

        """
        # 基本窗口
        self.root.title("Text查看器")
        self.root.geometry('800x600')
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)
        # 拖动文件
        windnd.hook_dropfiles(self.root, func=self.open_file)
        # 章节列表框架
        self.chapter_frame = ttk.Frame(self.root, padding="3")
        self.chapter_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.chapter_frame.rowconfigure(0, weight=1)
        # 章节信息

        # 具体内容框架
        self.content_frame = ttk.Frame(self.root, padding="3")
        self.content_frame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        # 具体内容
       
        # 设置栏
        status_frame = ttk.Frame(self.root, padding="3")
        status_frame.grid(column=0, columnspan=2, row=1, sticky=(N, W, E, S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=1)
        status_frame.columnconfigure(2, weight=1)
        # 设置栏按钮
        self.chapter_button = ttk.Button(status_frame, text="章节", command=self.show_chapter, state="disabled")
        self.chapter_button.grid(column=0, row=0, sticky=W)
        self.color_button = ttk.Button(status_frame, text="背景颜色", command=self.change_color, state="disabled")
        self.color_button.grid(column=2, row=0, sticky=E)
        self.bigger_button = ttk.Button(status_frame, text="+", command=self.bigger_font, state="disabled")
        self.bigger_button.grid(column=3, row=0, sticky=E)
        self.smaller_button = ttk.Button(status_frame, text="-", command=self.smaller_font, state="disabled")
        self.smaller_button.grid(column=4, row=0, sticky=E)

    def destroy(self):
        self.content_text.destroy()
        self.chapters_lb.destroy()

    def open_file(self, files):
        if self.text:
            self.destroy()
        try:
            filename = files[0].decode("utf-8")
            self.root.title(files[0].decode("utf-8"))
        except UnicodeDecodeError:
            filename = files[0].decode("gbk")
        finally:
            self.root.title(filename)
            self.text = content.Content(filename)
        # 具体内容
        self.content_text = Text(self.content_frame)
        self.content_text.grid(column=0, row=0, sticky=(N, W, E, S)) 
        self.content_text.insert("1.0", self.text.content)
        self.content_text.configure(font=font.Font(size=self.text.font_size))
        self.content_text.configure(state="disabled")
        content_scroll = ttk.Scrollbar(self.content_frame, orient=VERTICAL, command=self.content_text.yview)
        content_scroll.grid(column=1, row=0, sticky=(N, S))
        self.content_text.configure(yscrollcommand=content_scroll.set)
        # 章节信息
        v = StringVar()
        v.set(self.text.chapters)

        self.chapters_lb = Listbox(self.chapter_frame, listvariable=v)
        self.chapters_lb.grid(column=0, row=0, sticky=(N, W, E, S))
        self.chapters_lb.configure(background="#cccccc")
        self.chapters_lb.bind('<<ListboxSelect>>', self.select_chapter)
        chapter_scroll = ttk.Scrollbar(self.chapter_frame, orient=VERTICAL, command=self.chapters_lb.yview)
        chapter_scroll.grid(column=1, row=0, sticky=(N, S))
        self.chapters_lb.configure(yscrollcommand=chapter_scroll.set)

        # 是否显示章节
        if self.text.if_chapter:
            self.chapter_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        else:
            self.chapter_frame.grid_forget()

        # 使按钮有效
        self.chapter_button.configure(state="normal")
        self.color_button.configure(state="normal")
        self.bigger_button.configure(state="normal")
        self.smaller_button.configure(state="normal")

    def show_chapter(self, *args):
        if self.text.if_chapter:
            self.text.if_chapter = False 
            self.chapter_frame.grid_forget()
        else:
            self.text.if_chapter = True
            self.chapter_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    def change_color(self, *args):
        color = self.text.get_new_color()
        self.content_text.configure(background=color[1])
        self.content_text.configure(foreground=color[0])

    def bigger_font(self, *args):
        self.text.increase_size()
        self.content_text.configure(font=font.Font(size=self.text.font_size))

    def smaller_font(self, *args):
        self.text.decrease_size()
        self.content_text.configure(font=font.Font(size=self.text.font_size))

    def select_chapter(self, *args):
        idx = int(self.chapters_lb.curselection()[0])
        self.content_text.see(self.content_text.search(self.text.chapters[idx], 1.0))


tv = TV()