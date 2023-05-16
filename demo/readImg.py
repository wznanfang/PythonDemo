import os

# 读取文件夹下文件的名字
filepath = "C:/Users/Administrator/Pictures/uToolsWallpapers"
files = os.listdir(filepath)

for file in files:
    print(os.path.basename(file))



