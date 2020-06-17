# TextViewer：一个简单的小说阅读软件

支持txt文件，可以自动识别章节名称，更改阅读背景，编码格式，以及改变字体大小。

## 软件截图

![screenshot](\docs\screenshot.png)

## 可识别章节格式

可以参考项目中的`testRE.txt`文件

使用的正则表达式为

```python
PATTERN = re.compile(r'^[0-9]+\.?\s\S*|^第?[0-9一二三四五六七八九十百千]+[章节部]\s\S*', re.MULTILINE)
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

```
git clone https://github.com/zoemurmure/TextViewer.git
cd TextViewer
python setup.py install
```

之后在命令行输入`textviewer`就可以启动程序了