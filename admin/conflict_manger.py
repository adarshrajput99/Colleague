import os
import tkinter


def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


def write_logs(text):
    with open(curr_d() + '/Logs/stats', 'a') as my_file:
        my_file.write(text)


def read_logs():
    with open(curr_d() + '/Logs/temp_logs', 'r+') as my_file:
        return my_file.read()


def conflict_detected():
    root = tkinter.Tk()
    root.geometry("210x50")
    root.title("Conflict raised")
    error = tkinter.Label(root,text="oops there is an Error \n your connection might be slow")
    error.place(x=10, y=10)
    root.mainloop()


