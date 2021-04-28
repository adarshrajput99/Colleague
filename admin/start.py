from tkinter import *
# from admin import interface2
from admin import interface2


class start_page_1:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("500x500")
        self.root.maxsize(500, 500)
        self.root.minsize(500, 500)
        self.root.title("COLLEAGUE")
        photo = PhotoImage(file="asr.png")
        label = Button(image=photo, command=self.click)
        label.pack()
        self.root.bind('<Return>', self.click)
        self.root.mainloop()

    def click(self, event=None):
        self.root.destroy()
        interface2.interface_2()


if __name__ == "__main__":
    start_page_1()
