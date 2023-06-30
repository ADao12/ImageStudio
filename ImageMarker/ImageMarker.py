
import os
import platform
import tkinter as tk
import tkinterdnd2 as tk2
from tkinter import filedialog
from PIL import Image
from tkinterdnd2 import DND_FILES
print(tk.TkVersion)

class App(tk2.Tk):
    def __init__(self):
        super().__init__()
        self.title("图片规格标记器")
        self.geometry("500x300")
        
        # Create widgets
        self.prefix_label = tk.Label(self, text="Prefix:")
        self.prefix_label.pack()
        self.prefix_entry = tk.Entry(self, width=50)
        self.prefix_entry.insert(0, "款号")
        self.prefix_entry.pack()
        
        self.folder_button = tk.Button(self, text="选择文件夹", command=self.select_folder)
        self.folder_button.pack()
        
        self.start_button = tk.Button(self, text="开始", command=self.filter_files)
        self.start_button.pack()
        
        self.log_text = tk.Text(self)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Allow drag and drop
        # self.bind("<<Drop>>", self.drop_event)
        # self.bind("<<Drag_Enter>>", self.drag_enter_event)
        # self.bind("<<Drag_Leave>>", self.drag_leave_event)
        # self.bind("<<Drag_Ongoing>>", self.drag_ongoing_event)

        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.drop_event)
        
    def select_folder(self):
        self.folder_path = filedialog.askdirectory(initialdir=os.getcwd())
        self.log_text.insert(tk.END, "Selected folder: {}\n".format(self.folder_path))
        
    def filter_files(self):
        prefix = self.prefix_entry.get()
        if not hasattr(self, "folder_path"):
            self.log_text.insert(tk.END, "Please select a folder.\n")
            return
        
        # self.log_text.insert(tk.END, "Files in folder:\n")
        # for filename in os.listfile(self.folder_path):
            # self.log_text.insert(tk.END, "- {}\n".format(filename))
        self.process_folder(self.folder_path, prefix)

    def drop_files(self, files):
        self.folder_path = files[0]
        self.log_text.insert(tk.END, "Selected folder: {}\n".format(self.folder_path))
                
    def drop_event(self, event):
        self.folder_path = event.data.strip()
        self.log_text.insert(tk.END, "Selected folder: {}\n".format(self.folder_path))
        
    def drag_enter_event(self, event):
        event.widget.config(bg="gray")
        
    def drag_leave_event(self, event):
        event.widget.config(bg=self.cget("background"))
        
    def drag_ongoing_event(self, event):
        event.widget.config(bg="gray")
    
    # 定义检测和重命名文件函数
    def process_folder(self, folder_path, prefix):
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png'):
                    filepath = os.path.join(foldername, filename)
                    try:
                        fp = open(filepath, 'rb')
                        with Image.open(fp) as im:
                            width, height = im.size
                            size = os.path.getsize(filepath)
                            fp.close()
                            if (width != 1340 or height != 1785) and (width != 1200 or height != 1200) and (width != 80 or height != 80) and (size < 200000 or size > 2000000):
                                # new_filename = f"{prefix}_not_match_{filename}"
                                # os.rename(filepath, os.path.join(foldername, new_filename))
                                self.log_text.insert(tk.END, f'尺寸不匹配 {filename} 规格： {width} x {height}\n')
                            elif width == 1200 and height == 1200:
                                new_filename = f"{prefix}_正.png"
                                os.rename(filepath, os.path.join(foldername, new_filename))
                                self.log_text.insert(tk.END, f'Renamed {filename} to {new_filename}\n')
                            elif width == 80 and height == 80:
                                new_filename = f"{prefix}_色块.png"
                                os.rename(filepath, os.path.join(foldername, new_filename))
                                self.log_text.insert(tk.END, f'Renamed {filename} to {new_filename}\n')
                            else:
                                self.log_text.insert(tk.END, f'尺寸不匹配2 {filename} 规格： {width} x {height}\n')
                    except OSError as e:
                        fp.close()
                        self.log_text.insert(tk.END, f'{filename} has a problem: {e}')
        
if __name__ == "__main__":
    app = App()
    # if platform.system() == "Windows":
    #     from distutils.core import setup
    #     import py2exe
    #     setup(console=["app.py"])
    app.mainloop()
