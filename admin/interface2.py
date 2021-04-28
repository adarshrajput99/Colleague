from tkinter import *
from admin import interface3
from admin.project_manger import project_handel_func
from employee import user_start_4
from admin.cloud_manager import cloud_manger
import os
import sqlite3


def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


def encrypt(text):
    x = ""
    for i in text:
        x = x + chr(ord(i) + 111)
    return x


print(encrypt("hi"))


def decryption(text):
    x = ""
    for i in text:
        x = x + chr(ord(i) - 111)
    return x


def set_password():
    x = None
    print("Enter the emp_id: ")
    input(x)
    print("Enter the password:")
    key = input()
    print(key)
    db = sqlite3.connect(curr_d() + '/admin/oms.db')
    cursor = db.cursor()
    db.execute(
        "INSERT INTO pass(emp_id,key) VALUES(?,?)",
        (x, encrypt(key)))
    db.commit()


def read_pass(id, key):
    x = []
    db = sqlite3.connect(curr_d() + '/admin/oms.db')
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM pass WHERE emp_id=?", (id,))
        records = cursor.fetchall()
        for row in records:
            for i in range(len(row)):
                x.append(row[i])
    except Exception as e:
        return False
    print(decryption(x[1]))
    print(key)
    if str(decryption(x[1])) == str(key):
        return True
    else:
        return False


class interface_2:
    def __init__(self):
        self.text = ""
        staus = True
        self.c = cloud_manger()
        self.p = project_handel_func()
        if self.c.database_sync_get():
            self.text = "Your network is slow"
            staus = False
        else:
            self.text = "* Denotes mandatory\n Collect you Password and \nEmp_id from Admin\n\nWelcome to Colleague"

        call_id = 0
        self.root = Tk()
        # OK FUNCTION DEFINITION WHICH IS USED IN LAYOUT
        self.root.title("SIGN IN")
        self.root.geometry("500x500")
        self.root.bind('<Return>', self.ok)
        photo = PhotoImage(file=curr_d() + "/icons/background.png")
        background_label = Label(self.root, image=photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABELS
        user = Label(self.root, text="User_Id  ", fg="white", bg="black")
        password = Label(self.root, text="Password", fg="white", bg="black")

        self.response = Label(self.root, text=self.text, fg="white", bg="black")
        self.response.place(x=165, y=320)
        user.place(x=130, y=220)
        password.place(x=130, y=250)
        self.user_val = StringVar()
        self.pass_val = StringVar()

        #   TEXT FIELD
        user_e = Entry(self.root, textvariable=self.user_val, fg="white", bg="grey11")
        password_e = Entry(self.root, textvariable=self.pass_val, show="*", fg="white", bg="grey11")
        user_e.place(x=198, y=220)
        password_e.place(x=198, y=250)

        # BUTTON
        b1 = Button(self.root, text="ok", command=self.ok, width=25, fg="white", bg="black")
        if staus:
            b1.place(x=135, y=280)

        self.root.mainloop()

    def ok(self, event=None):
        pass
        if self.user_val.get() == "asr":
            if self.pass_val.get() == "asr":
                self.response.config(text="access granted")
                self.root.destroy()
                try:
                    interface3.interface_3()
                except EXCEPTION as e:
                    print("Network Error")
                    # self.response.config(text="Network Error")
            else:
                self.response.config(text="access denied!!!")
        else:
            if read_pass(int(self.user_val.get()),self.pass_val.get()):
                self.root.destroy()
                user_start_4.user_start(int(self.user_val.get()))
            else:
                self.response.config(text="access denied!!!")


if __name__ == "__main__":
    interface_2()
