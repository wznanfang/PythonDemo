import os
import shutil

# 读取文件夹下文件的名字
filepath = "E:/shuju/5000"
files = os.listdir(filepath)

#遍历文件并根据后缀名分类
# jpg_list = []
# png_list = []
# jpeg_list = []
# other_list = []
#
# for file in files:
#     # print(os.path.basename(file))
#     if os.path.basename(file).endswith('.jpg'):
#         jpg_list.append(os.path.basename(file))
#         # 如果文件名的后缀是png，则将其添加到png_list中
#     elif os.path.basename(file).endswith('.png'):
#         png_list.append(os.path.basename(file))
#         # 如果文件名的后缀是gif，则将其添加到gif_list中
#     elif os.path.basename(file).endswith('.jpeg'):
#         jpeg_list.append(os.path.basename(file))
#     else:
#         other_list.append(os.path.basename(file))
# print(jpg_list)
# print(png_list)
# print(jpeg_list)
# print(other_list)

# 将一个文件夹的5000张图片分别存储到5个文件夹中，每个文件夹1000张图片
# 目标文件夹路径
src_dir = 'E:/shuju/5000'
dest_dirs = ["E:/shuju/1000-1", "E:/shuju/1000-2", "E:/shuju/1000-3", "E:/shuju/1000-4", "E:/shuju/1000-5"]

# Create the destination directories if they don't already exist
for dest_dir in dest_dirs:
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

file_count = 0
for filename in os.listdir(src_dir):
    if (filename.endswith(".jpg")) or (filename.endswith(".png")) or (filename.endswith(".jpeg")):
        src_path = os.path.join(src_dir, filename)
        dest_dir = dest_dirs[file_count // 1000]
        dest_path = os.path.join(dest_dir, filename)
        shutil.copy(src_path, dest_path)
        file_count += 1
