import glob
from tkinter import *

import admin.cloud_manager
import admin.employee_manger
import admin.file
import admin.project_manger
from employee.face_recognition import *


def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


class user_start:
    def __init__(self, emp_id):
        self.emp_id = emp_id
        self.root = Tk()
        self.root.geometry("1010x380")
        self.root.maxsize(1010, 380)
        self.root.minsize(1010, 380)
        self.root.title("User Handel")
        admin.employee_manger.sync(1)
        self.get_mail = admin.cloud_manager.cloud_manger()
        instance = admin.project_manger.project_handel_func()
        instance_manger = admin.employee_manger.emp_manage_functions()

        def start_here():
            self.root.destroy()
            starter(self.emp_id)

            # starter(self.emp_id)

        photo = PhotoImage(file=curr_d() + "/employee/icons8-export-20.png")
        upload_pic = PhotoImage(file=curr_d() + "/icons/upload.png")
        download_pic = PhotoImage(file=curr_d() + "/icons/download.png")
        mail_pic = PhotoImage(file=curr_d() + "/icons/mail.png")
        start_pic = PhotoImage(file=curr_d() + "/icons/start.png")
        done = PhotoImage(file=curr_d() + "/icons/done.png")
        black_label = Label(text="", bg="black", width=1000, height="4", borderwidth=0)
        black_label.place(x=0, y=0)

        user_id_lb = Label(text="User_id :", fg="white", bg="black")
        user_id = Entry(self.root)
        user_name_lb = Label(text="User Name :", fg="white", bg="black")
        user_name = Entry(self.root)
        user_join_lb = Label(text="Joined on :", fg="white", bg="black")
        user_join = Entry(self.root)
        grade_lb = Label(text="Grade :", fg="white", bg="black")
        grade = Entry(self.root)

        sal_lb = Label(self.root, text="Your salary will be in range: ", font=('Helvetica', 18, 'bold'), fg="white",
                       bg="black")
        start_lb = Label(text="Start from  :")
        end_lb = Label(text="Upto           :")
        file_lb = Label(text="Project", font=('Helvetica', 20, 'bold'), fg="white", bg="black")
        feedback_lb = Label(text="Feedback:(For last submission)", font=('Helvetica', 15, 'bold'))
        start = Entry(self.root)
        end = Entry(self.root)
        feedback = Text(self.root, bg='gray20', fg='white', font=('Helvetica', 15))
        upload = Button(text="UPLOAD FILES", width=180, height=50,
                        font=('Helvetica', 11, 'bold'),
                        bg='gray16', fg='white', command=self.file_get_upload, image=upload_pic)
        download = Button(text="DOWNLOAD FILES", width=180, height=50,
                          font=('Helvetica', 11, 'bold'), bg='gray16', fg='white', command=self.file_get_download,
                          image=download_pic)
        self.date = Label(text='')
        # Face recognition stop function
        Logout = Button(image=photo, command=lambda: [f() for f in [stop(emp_id), exit(0)]], relief="flat")
        mail_bt = Button(text="", width=180, height=50,
                         font=('Helvetica', 11, 'bold'), bg='gray16', fg='white',
                         image=mail_pic, command=self.send_mails)
        mail_bt.place(x=800, y=70)
        session_start = Button(text="Start session", width=180, height=50, bg='gray16', fg='white', command=start_here,
                               image=start_pic)
        session_start.place(width=100, height=218)
        session_start.place(x=320, y=160)

        self.date.place(x=840, y=38)
        self.root.after(100, self.clock)
        user_id_lb.place(x=0, y=0)
        user_id.place(x=60, y=0)
        user_name_lb.place(x=250, y=0)
        user_name.place(x=335, y=0)
        user_join_lb.place(x=520, y=0)
        user_join.place(x=590, y=0)
        grade_lb.place(x=775, y=0)
        grade.place(x=825, y=0)
        sal_lb.place(x=0, y=30)
        start_lb.place(x=0, y=70)
        end_lb.place(x=0, y=92)
        start.place(x=75, y=70)
        end.place(x=75, y=92)
        upload.place(x=400, y=70)
        download.place(x=600, y=70)
        file_lb.place(x=550, y=30)
        feedback.place(x=2, y=160)
        feedback.place(width=300, height=218)
        feedback_lb.place(x=0, y=130)
        Logout.place(x=971, y=341)

        # Working project
        project = Label(text="Project Details", font=('Helvetica', 16, 'bold', 'underline'))
        project.place(x=620, y=130)
        # LABEL
        project1 = Label(text="\n    Active project  :\t\t\t\t   \n\n\tDue to  :\t\t\t\t   \n\n\tStatus :\t\t\t\t "
                              "\n\n\tLast file upload :\t\t\t\t\t\n", font=('Helvetica', 12, 'bold'), anchor="s",
                         borderwidth=2, relief="solid")
        project1.place(x=440, y=160)

        # Project Fields
        project_active = Entry(self.root)
        project_active.place(width=290)
        project_active.place(x=650, y=175)

        project_due = Entry(self.root)
        project_due.place(width=290)
        project_due.place(x=650, y=210)

        project_status = Entry(self.root)
        project_status.place(width=290)
        project_status.place(x=650, y=245)

        project_last_file = Entry(self.root)
        project_last_file.place(width=290)
        project_last_file.place(x=650, y=280)
        x = instance_manger.get_full_emp_record(emp_id)
        sal = instance_manger.sal_get(emp_id)

        proj_list = instance.get_emp_proj(int(emp_id))
        project_last_file.insert(END, instance_manger.last_change(int(emp_id)))
        try:
            user_id.insert(END, emp_id)
            user_name.insert(END, x[1])
            user_join.insert(END, x[4])
            grade.insert(END, x[3])
            start.insert(END, sal[1])
            end.insert(END, sal[2])
            try:
                project_status.insert(END, proj_list[4])
                project_due.insert(END, proj_list[3])
                project_active.insert(END, proj_list[1])
            except:
                project_status.insert(END, "No project")
                project_due.insert(END, "No project")
                project_active.insert(END, "No project")
            if x[7] == "No Feedback":
                feedback.insert(END, "No Feedback")
            else:
                feedback.insert('1.0', x[7])
            feedback.config(state="disabled")
        except Exception as e:
            print(e)

        mail_exist = Button(self.root, text="Check for Mails", bg="DodgerBlue2", fg="white",
                            font=('Helvetica', 15, 'bold'),
                            command=lambda: [f() for f in [self.read_logs]])
        mail_exist.configure(width=44, height=2)
        mail_exist.place(x=440, y=320)

        Mark_Done = Button(text="", width=60, height=143, bg='gray15', fg='white', image=done,
                           command=lambda: [f() for f in [instance_manger.mark_myProject_Done(self.emp_id)]])
        Mark_Done.place(x=444, y=165)
        self.root.protocol("WM_DELETE_WINDOW", lambda: [f() for f in [stop(emp_id), exit(0)]])

        self.root.mainloop()

    def read_logs(self):
        def close():
            import os
            import shutil
            shutil.rmtree(curr_d() + "/Logs/mail")
            os.mkdir(curr_d() + "/Logs/mail")

        close()
        root = Tk()
        root.geometry("300x80")
        root.title("Mails")
        self.get_mail.mail_getter(self.emp_id)
        print("got out")
        print(os.chdir(curr_d() + "/Logs/mail/"))
        list_mails = glob.glob("*")
        print(list_mails)
        var = StringVar(root)
        var.set("Available Mails")
        try:
            get_file_fd = OptionMenu(root, var, *list_mails)
        except Exception as e:
            get_file_fd = OptionMenu(root, var,"no mails")
        get_file_fd.config(text="Avaialable files", width=28, height=1, font=('Helvetica', 12))
        get_file_fd.place(x=0, y=0)
        try:
            open = Button(root, text="Open", width=34, command=lambda: [f() for f in [self.file_open(var.get()), close()]])
            open.place(x=0, y=40)
        except Exception as e:
            print(e)

        root.mainloop()

    def file_open(self, file):
        print(file)
        root = Tk()
        root.geometry("800x400")
        root.title(file)
        make = Text(root, bg='gray20', fg='white', font=('Helvetica', 15))
        make.place(x=0, y=0)
        try:
            with open(curr_d() + '/mail/' + str(file), 'r+') as my_file:
                z = (my_file.read())
                make.insert(END, z)
        except Exception as e:
            print(e)
        root.mainloop()

    def erase(self, file=""):
        try:
            os.remove(curr_d() + '/Logs/mail/' + str(file))
        except:
            for file_get in glob.glob("*"):
                os.remove(curr_d() + '/Logs/mail/' + str(file_get))

    def send_mails(self):

        root = Tk()
        root.geometry("800x440")
        root.title("Mails")
        make = Text(root)
        make.place(width=800, height=400)
        make.place(x=0, y=0)
        make.insert(END, "Type your mail here")
        sending_lb = Label(root, text="Receiver emp_id :", font=('Helvetica', 14, 'bold'))
        sending_lb.place(x=30, y=405)
        sending_fd = Entry(root)

        def send_mail():
            with open(curr_d() + '/Logs/mail_send/mail_temp', 'r+') as my_file:
                my_file.truncate(0)
                my_file.write(make.get("1.0", END))
            self.get_mail.file_uploader(sending_fd.get(), self.emp_id)

        sending_fd.place(y=405, x=200)
        send = Button(root, text="Send", bg="black", fg="white", font=('Helvetica', 12, 'bold'), command=send_mail)
        send.place(width=100, height=30)
        send.place(x=690, y=405)
        cancel = Button(root, text="Cancel", bg="black", fg="white", font=('Helvetica', 12, 'bold'))
        cancel.place(width=100, height=30)
        cancel.place(x=580, y=405)
        root.mainloop()

    def clock(self):
        t = time.strftime('%d/%m/%Y, %H:%M:%S', time.localtime())
        if t != '':
            self.date.config(text=t, font=('Helvetica', 12, 'bold'), fg="white", bg="black")
        self.root.after(100, self.clock)

    def file_get_upload(self):
        u = admin.file.file_interface_upload(self.emp_id)

    def file_get_download(self):
        try:
            d = admin.file.file_interface_download(self.emp_id)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    user_start(1211)
