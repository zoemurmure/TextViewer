import sys, os
#from textviewer import tv
import tv

def main():
    # 创建保存历史记录的文件夹
    history_path = os.path.join(os.path.expanduser('~'), "AppData", "Local", "TextViewer")
    if not os.path.exists(history_path):
        os.mkdir(history_path)

    if len(sys.argv) > 1:
        tv.TV(history_path, sys.argv[1])
    else:
        tv.TV(history_path)


if __name__=="__main__":
    main()