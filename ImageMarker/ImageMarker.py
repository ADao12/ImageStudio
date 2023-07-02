import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinterdnd2 as tk2
from tkinterdnd2 import DND_FILES
import os

class App(tk2.Tk):
    def __init__(self):
        super().__init__()
        self.title("图片尺寸名字修改器")
        self.geometry("600x400")

        # 创建GUI控件
        self.size1_label = tk.Label(self, text="尺寸1:")
        self.size1_entry = tk.Entry(self, width=10)
        self.filename1_label = tk.Label(self, text="文件名1:")
        self.filename1_entry = tk.Entry(self, width=20)

        self.size2_label = tk.Label(self, text="尺寸2:")
        self.size2_entry = tk.Entry(self, width=10)
        self.filename2_label = tk.Label(self, text="文件名2:")
        self.filename2_entry = tk.Entry(self, width=20)

        self.folder_button = tk.Button(self, text="选择文件夹", command=self.select_folder)
        self.start_button = tk.Button(self, text="开始", command=self.process_files)
        self.log_text = tk.Text(self, width=50, height=10)

        # 布局控件
        self.size1_label.grid(row=0, column=0, padx=5, pady=5)
        self.size1_entry.grid(row=0, column=1, padx=5, pady=5)
        self.filename1_label.grid(row=0, column=2, padx=5, pady=5)
        self.filename1_entry.grid(row=0, column=3, padx=5, pady=5)

        self.size2_label.grid(row=1, column=0, padx=5, pady=5)
        self.size2_entry.grid(row=1, column=1, padx=5, pady=5)
        self.filename2_label.grid(row=1, column=2, padx=5, pady=5)
        self.filename2_entry.grid(row=1, column=3, padx=5, pady=5)

        self.folder_button.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.start_button.grid(row=2, column=3, padx=5, pady=5, sticky="E")

        self.log_text.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

        # 设置默认值
        self.size1_entry.insert(0, "80x80")
        self.filename1_entry.insert(0, "款号_色块")
        self.size2_entry.insert(0, "1200x1200")
        self.filename2_entry.insert(0, "款号_正")

        # 自适应布局
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.relative_path = ""

        # 设置日志文本格式
        self.folder_path_text_tag = "folder_path_text_tag"
        self.log_text.tag_config(self.folder_path_text_tag, foreground="blue")
        self.unprocessed_file_text_tag = "unprocessed_file_text_tag"
        self.log_text.tag_config(self.unprocessed_file_text_tag, foreground="red")

        # 设置窗口的拖拽事件处理函数
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.drag_and_drop_folder)

    def drag_and_drop_folder(self, event):
        if event.widget is self:
            if event.data:
                folder_path = event.data.strip().replace("{","").replace("}","")
                self.init_folder(folder_path)
        else:
            event.widget.destroy()



    def select_folder(self):
        folder_path = filedialog.askdirectory(initialdir=os.getcwd())
        self.init_folder(folder_path)
    
    def init_folder(self, folder_path):
        self.folder_path = folder_path
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"选择文件夹: {folder_path}\n", self.folder_path_text_tag)
        self.log_text.config(state=tk.DISABLED)
        self.relative_path = "/" + self.relpath(self.folder_path, ":/")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"相对地址: {self.relative_path}\n", self.folder_path_text_tag)
        self.log_text.config(state=tk.DISABLED)
 
    def process_files(self):
        folder_path = self.folder_path
        size1 = self.size1_entry.get()
        filename1 = self.filename1_entry.get()
        size2 = self.size2_entry.get()
        filename2 = self.filename2_entry.get()

        # 遍历文件夹
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                # 检查文件类型是否为图片
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    filepath = os.path.join(root, filename)
                    unprocessed_file_path = self.relpath(filepath, self.relative_path)
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, f"无法处理的文件: {unprocessed_file_path}\n", self.unprocessed_file_text_tag)
                    self.log_text.config(state=tk.DISABLED)
                    continue
                    
                # 检查文件大小是否符合要求
                filepath = os.path.join(root, filename)
                try:
                    with Image.open(filepath) as img:
                        width, height = img.size
                except:
                    unprocessed_file_path = self.relpath(filepath, self.relative_path)
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, f"无法处理的文件: {unprocessed_file_path}\n", self.unprocessed_file_text_tag)
                    self.log_text.config(state=tk.DISABLED)
                    continue
                    
                if f"{width}x{height}" == size1:
                    new_filename = filename.replace(os.path.splitext(filename)[0], filename1)
                    new_filepath = os.path.join(root, new_filename)
                    os.rename(filepath, new_filepath)
                    old_path = self.relpath(filepath, self.relative_path)
                    new_path = self.relpath(new_filepath, self.relative_path)
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, f"{old_path} --> {new_path}\n")
                    self.log_text.config(state=tk.DISABLED)
                elif f"{width}x{height}" == size2:
                    new_filename = filename.replace(os.path.splitext(filename)[0], filename2)
                    new_filepath = os.path.join(root, new_filename)
                    os.rename(filepath, new_filepath)
                    old_path = self.relpath(filepath, self.relative_path)
                    new_path = self.relpath(new_filepath, self.relative_path)
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, f"{old_path} --> {new_path}\n")
                    self.log_text.config(state=tk.DISABLED)
    
    def relpath(self, origin_path, relative_path):
        new_path = origin_path.split(relative_path)[1]
        # self.log_text.config(state=tk.NORMAL)
        # self.log_text.insert(tk.END, f"{origin_path} del {relative_path} --> {new_path}\n")
        # self.log_text.config(state=tk.DISABLED)
        return new_path



if __name__ == "__main__":
    app = App()
    app.mainloop()
