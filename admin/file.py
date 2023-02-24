import tkinter
from tkinter import filedialog
import time
from admin.cloud_manager import cloud_manger
from admin.employee_manger import emp_manage_functions
import os
from employee.user_start_4 import user_start
from admin.conflict_handel import conflict_handler
from admin.conflict_manger import conflict_detected


def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


class file_interface_upload:
    def __init__(self, emp_id):
        self.instance_emp_mange = emp_manage_functions()
        self.cloud_manger_instance = cloud_manger()
        self.emp_id_instance = emp_id
        self.t = time.strftime('%d/%m/%Y, %H:%M:%S', time.localtime())
        self.main_win = tkinter.Tk()
        self.main_win.geometry("335x100")
        self.main_win.title("SELECT FILE")
        self.main_win.sourceFile = ''

        self.b_chooseFile = tkinter.Button(self.main_win, text="Choose File",
                                           command=self.chooseFile,
                                           font=('Helvetica', 11, 'bold'))
        self.upload = tkinter.Button(self.main_win, text="UPLOAD", width=38, command=self.up)
        self.b_chooseFile.place(x=0, y=0)
        self.b_chooseFile.width = 100
        self.upload.place(x=0, y=30)
        self.response = tkinter.Label(self.main_win, text="Select the file and wait for response ")
        self.response.place(x=45, y=60)
        self.field = tkinter.Entry(self.main_win)
        self.field.place(width=200)
        self.field.place(x=130, y=3)

    def chooseFile(self):
        self.main_win.sourceFile = filedialog.askopenfilename(parent=self.main_win, initialdir="/home",
                                                              title='Please select a directory')
        self.field.insert(tkinter.END, self.main_win.sourceFile)

    def up(self):
        try:
            print(type(self.main_win.sourceFile))
            self.cloud_manger_instance.upload(self.main_win.sourceFile)
            conflict_handler("#{/*UPLOAD*/" + self.t + "->" + self.main_win.sourceFile + "}",
                            self.emp_id_instance)
            self.response.config(text="done")

        except Exception as e:
            self.response.config(text=e)
            conflict_detected()

    def end(self):
        if self.emp_id_instance != 0:
            self.main_win.destroy()
            user_start(self.emp_id_instance)
        else:
            self.main_win.destroy()

    def on_closing(self):
        self.main_win.destroy()

        self.main_win.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main_win.mainloop()
        self.cloud_manger_instance.upload(self.main_win.sourceFile)

    def finish(self):
        self.main_win.destroy()
        return self.emp_id_instance


class file_interface_download:
    def __init__(self, emp_id):
        self.instance_emp_mange = emp_manage_functions()
        self.cloud_manger_instance = cloud_manger()
        list_files = self.cloud_manger_instance.available_files()
        self.t = time.strftime('%d/%m/%Y, %H:%M:%S', time.localtime())
        self.emp_id = emp_id
        self.root = tkinter.Tk()
        self.root.geometry("300x125")
        self.root.title("File Download")
        self.get_f = tkinter.Label(self.root, text="Get available files", font=('Helvetica', 12, "bold"))
        self.get_f.place(x=80, y=0)
        self.var = tkinter.StringVar(self.root)
        try:
            self.get_file_fd = tkinter.OptionMenu(self.root, self.var, *list_files)
        except Exception as e:
            print(e)
            return
        self.get_file_fd.config(text="Avaialable files", width=28, height=1, font=('Helvetica', 12))
        self.get_file_fd.place(x=0, y=35)
        self.var.set("Avail files")
        self.get = tkinter.Button(self.root, text="Download", command=self.ok, width=10)
        self.get.place(x=40, y=68)
        self.close = tkinter.Button(self.root, text="CLOSE", command=self.close, width=10)
        self.close.place(x=155, y=68)
        self.file_path = tkinter.Label(self.root, text="File path")
        self.file_path_fd = tkinter.Entry(self.root)
        self.file_path.place(x=0, y=100)
        self.file_path_fd.place(width=230)
        self.file_path_fd.place(x=65, y=100)
        self.file_path_fd.insert(tkinter.END, os.path.expanduser("~") + "/Downloads/")

        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def ok(self):
        try:
            print(str(self.var.get()))
            self.cloud_manger_instance.download(str(self.var.get()))
            conflict_handler("#{/*DOWNLOAD*/" + self.t + "->" + str(self.var.get()) + "}", self.emp_id)
            self.get_f.config(text="Done")
        except Exception as e:
            self.get_f.config(text=e)
            conflict_detected()

    def reverse(self):
        self.root.destroy()
        x = user_start(self.emp_id)
