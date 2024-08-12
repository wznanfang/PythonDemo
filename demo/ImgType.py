import os
import shutil
import tkinter as tk
from tkinter import filedialog

import magic
import ttkbootstrap as ttk

# 文件类型到文件夹的映射
type_to_folder = {
    'text/plain': 'text',
    'application/pdf': 'pdf',
    'image/jpeg': 'img',
    'image/png': 'img',
    'image/webp': 'img',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'excel',
    'application/vnd.ms-excel': 'excel',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'word',
    'application/msword': 'word',
    'application/vnd.ms-powerpoint': 'powerpoint',
    'application/zip': 'zip',
    'video/mp4': 'video',
    'audio/mpeg': 'audio',
}

# 创建主界面
root = tk.Tk()
root.title("文件分类器")
root.configure(bg='#d3d8de')
# 设置窗口大小和固定
root.geometry("490x410")  # 设置窗口的初始大小为 300x120 像素
root.resizable(False, False)  # 禁止窗口调整大小

mime = magic.Magic(mime=True)
selected_folder = None
style = ttk.Style()

# 计数器字典，用于不同类型文件的计数
file_counters = {folder: 1 for folder in type_to_folder.values()}


def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        log_text.insert(tk.END, f"选择的文件夹路径为: {folder_path}\n")
        start_button.config(state=tk.NORMAL)
        global selected_folder
        selected_folder = folder_path


def start_classification():
    prefix = prefix_entry.get().strip()  # 获取用户输入的前缀
    classify_files_in_folder(selected_folder, prefix)


tk.Label(root, text="文件名前缀:").place(x=10, y=20, width=80, height=30)
prefix_entry = tk.Entry(root)
prefix_entry.place(x=85, y=20, width=120, height=30)

ttk.Button(root, text="选择文件夹", command=select_folder, style='primary-outline').place(x=260, y=20, width=100, height=30)

start_button = ttk.Button(root, text="开始分类", command=start_classification, state=tk.DISABLED, style='success-outline')
start_button.place(x=370, y=20, width=100, height=30)

log_text = tk.Text(root)
log_text.place(x=20, y=70, width=450, height=300)
log_text.configure(bg='#d8f0e0')
log_text.insert(tk.END, "--------------------执行日志打印--------------------\n")

# 静态文本
tk.Label(root, text="一个简易的文件分类工具", bg='#dfe4ea').place(x=150, y=375, width=140, height=30)


def classify_files_in_folder(folder_selected, prefix):
    log_text.insert(tk.END, f"----------开始分类文件夹【 {folder_selected} 】----------\n\n")

    for root, _, files in os.walk(folder_selected):
        for filename in files:
            filepath = os.path.join(root, filename)
            mime_type = mime.from_file(filepath)
            log_text.insert(tk.END, f'文件【 {filename} 】类型为: {mime_type}\n')

            target_folder = type_to_folder.get(mime_type, 'other')
            parent_folder = os.path.dirname(folder_selected)
            target_folder_path = os.path.join(parent_folder, target_folder)
            os.makedirs(target_folder_path, exist_ok=True)

            # 检查目标文件夹是否在计数器中
            if target_folder not in file_counters:
                file_counters[target_folder] = 1

            # 构造新的文件名
            if prefix:
                new_filename = f"{prefix}-{file_counters[target_folder]}.{filename.split('.')[-1]}"
            else:
                new_filename = f"{file_counters[target_folder]}.{filename.split('.')[-1]}"
            target_file_path = os.path.join(target_folder_path, new_filename)

            # 移动文件并重命名
            shutil.move(filepath, target_file_path)
            log_text.insert(tk.END, f"移动并重命名文件【 {filename} 】至【 {target_folder} 】文件夹中\n\n")

            # 更新计数器
            file_counters[target_folder] += 1

    log_text.insert(tk.END, "--------------------分类完成--------------------\n\n")
    start_button.config(state=tk.DISABLED)
    file_counters.clear()


# 运行主循环
root.mainloop()
