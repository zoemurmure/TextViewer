# TextViewer：一个简单的小说阅读软件

支持txt文件，可以自动识别章节名称，显示阅读百分比，更改阅读背景，编码格式，以及改变字体大小。具体功能查看下面的**版本更新说明**。

## 软件截图

![screenshot](https://github.com/zoemurmure/TextViewer/blob/master/docs/screenshot.png)

## 可识别章节格式

可以参考项目中的`testRE.txt`文件

使用的正则表达式为

```python
PATTERN = re.compile(r'^\s*[0-9]+[\.、]?\s\S*|^\s*第?[0-9一二三四五六七八九十百千]+[章节部]\s\S*|^\s*chapter\s*[0-9]+\s\S*', re.MULTILINE)
```

## 可设置的背景颜色

白色

护眼绿

深蓝

## 可设置的编码格式

ascii

gbk

utf-8

gb2312

utf-16

## EXE文件生成方法

```bash
pyinstaller -w -F .\run.py -i ./icon/favicon.ico
```

在`textviewer`子目录下输入上面的命令

**软件运行时会在用户目录下的`AppData/Local/TextViewer`中生成一个history文件用于记录历史信息**

## 版本更新说明

### 1.0

基本的TXT文件阅读功能，可以设置背景颜色，自动识别章节名称，选择编码方式，调整字体大小，空格键翻页

### 1.1

修复编码识别失败的漏洞

增加了显示阅读百分比功能

增加可识别章节名类型

增加行间距，优化阅读体验

添加了新的快捷键，支持左右键翻页以及上下键移动

窗口启动自动最大化（windows 和 Mac OS X）

优化启动模式，启动后不再保留命令行

### 2.0 最终放弃版本...

放弃了setup.py的安装方法，使用Pyinstaller单独生成了exe文件放入了release中，可自行下载

修改默认编码为gbk

增加命令行参数，从命令行直接传入需要打开的文件路径

content_text的优化，研究delete功能

title只显示文件名

添加了icon图标

加入历史记录功能(这个功能有一些问题，由于tkinter会异步调整字体高度，导致yview返回的值在未调整完之前一直在变，所以记录的阅读历史会存在误差)

#### 放弃原因

由于历史记录功能无法完善，始终没有在官方文档中找到其他获取显示位置的方法（如果有请一定要告诉我），所以决定专用wxpython重写一遍这个软件

#### wxpython

这个之后会另起一个项目