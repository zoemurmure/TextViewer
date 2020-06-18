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

## 安装方法

```bash
git clone https://github.com/zoemurmure/TextViewer.git
cd TextViewer
python setup.py install
```

之后在命令行输入`textviewer`就可以启动程序了

## 卸载

```bash
pip uninstall textviewer
```

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