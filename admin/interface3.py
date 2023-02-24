from tkinter import *

from admin import file
from admin.cloud_manager import cloud_manger
from admin.details import details
import os


def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


class interface_3:
    def __init__(self):
        self.root = Tk()
        self.c = cloud_manger()
        self.c.database_sync_get()
        from admin import employee_manger, project_manger
        self.e = employee_manger.emp_manage_functions()
        self.p = project_manger.project_handel_func()
        emp_id = 0
        self.root.geometry("1000x589")
        self.root.title("ADMIN HANDLE")
        photo = PhotoImage(file=curr_d() + "/icons/admin_bg.png")
        background_label = Label(self.root, image=photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # LABELS
        head = Label(self.root, text="Menu", font=('Helvetica', 18, 'bold', 'underline'), bg='black', fg='white')
        head.place(x=460, y=40)
        # BUTTON
        project = Button(self.root, text="Rooms list", width=20, height=2, bg='black', fg='white',
                         font=('Helvetica', 11, 'bold'),
                         command=project_manger.proj_list)
        project.place(x=0, y=390)
        emp = Button(self.root, text="User perf", width=20, height=2, bg='black', fg='white',
                     font=('Helvetica', 11, 'bold'), command=employee_manger.emp_performance_set)
        emp.place(x=0, y=75)
        add = Button(self.root, text="Add user", width=20, height=2, bg='black', fg='white',
                     font=('Helvetica', 11, 'bold'), command=employee_manger.add_emp)
        add.place(x=0, y=120)
        remove = Button(self.root, text="Remove  User", width=20, height=2, bg='black', fg='white',
                        font=('Helvetica', 11, 'bold'),
                        command=employee_manger.del_emp)
        remove.place(x=0, y=165)
        assign = Button(self.root, text="Add Room", width=20, height=2, bg='black', fg='white',
                        font=('Helvetica', 11, 'bold'), command=project_manger.add_new_project)
        assign.place(x=0, y=210)
        emp_grade = Button(self.root, text="Room List", width=20, height=2, bg='black', fg='white',
                           font=('Helvetica', 11, 'bold'), command=employee_manger.complete_emp_list)
        emp_grade.place(x=0, y=255)
        search = Button(self.root, text="Search", width=20, height=2, bg='black', fg='white',
                        font=('Helvetica', 11, 'bold'),
                        command=details)
        search.place(x=0, y=300)

        feedback = Button(self.root, text="Feedback", width=20, height=2, bg='black', fg='white',
                          font=('Helvetica', 11, 'bold'),
                          command=employee_manger.feedback)
        feedback.place(x=810, y=119)

        set_meeting_id = Button(self.root, text="Meeting id", width=20, height=2, bg='black', fg='white',
                                font=('Helvetica', 11, 'bold'),
                                command=self.meeting_id)
        set_meeting_id.place(x=810, y=255)
        enter_meeting = Button(self.root, text="Meeting id", width=20, height=2, bg='black', fg='white',
                               font=('Helvetica', 11, 'bold'),
                               command=self.meeting_id)
        enter_meeting.place(x=810, y=255)
        self.site_var = StringVar()
        self.site_var.set("Set down")
        self.site_down = Button(self.root, textvariable=self.site_var, width=20, height=2, bg='black', fg='white',
                                font=('Helvetica', 11, 'bold'), command=self.site)
        self.site_down.place(x=810, y=164)

        emp_working = Label(text="No. of Active user   :", font=('Helvetica', 11, 'bold'), fg="white", bg="black")
        emp_working.place(x=300, y=80)
        emp_working_fd = Entry(self.root)
        emp_working_fd.place(x=500, y=80)
        emp_working_fd.insert(END, self.e.get_no_of_emp())

        total_proj = Label(text="Total no of Active Room     :", font=('Helvetica', 11, 'bold'), fg="white", bg="black")
        total_proj.place(x=300, y=110)
        total_proj_fd = Entry(self.root)
        total_proj_fd.place(x=500, y=110)
        total_proj_fd.insert(END, self.p.get_no_of_proj())

        total_proj_active = Label(text="Finished Rooms     :", font=('Helvetica', 11, 'bold'), fg="white",
                                  bg="black")
        total_proj_active.place(x=300, y=140)
        total_proj_active_fd = Entry(self.root)
        total_proj_active_fd.place(x=500, y=140)
        total_proj_active_fd.insert(END, self.p.get_no_of_proj_done())

        dropbox_token = Label(text="Dropbox Token          :", font=('Helvetica', 11, 'bold'), fg="white", bg="black")
        dropbox_token.place(x=300, y=170)
        dropbox_token_fd = Entry(self.root)
        dropbox_token_fd.place(x=500, y=170)
        dropbox_token_fd.insert(END, self.c.token)

        database_check_employee = Label(text="User database check :", font=('Helvetica', 11, 'bold'), fg="white",
                                        bg="black")
        database_check_employee.place(x=300, y=200)
        database_check_employee_fd = Entry(self.root)
        database_check_employee_fd.place(x=500, y=200)
        if self.e.get_no_of_emp() != "0":
            database_check_employee_fd.insert(END, "Connected")
        else:
            database_check_employee_fd.insert(END, "Not connected")

        database_check_project = Label(text="Rooms database check  :", font=('Helvetica', 11, 'bold'), fg="white",
                                       bg="black")
        database_check_project.place(x=300, y=230)
        database_check_project_fd = Entry(self.root)
        database_check_project_fd.place(x=500, y=230)
        if self.p.get_no_of_proj_done() != "0":
            database_check_project_fd.insert(END, "Connected")
        else:
            database_check_project_fd.insert(END, "Not connected")

        database_check_salary = Label(text="Files database check    :", font=('Helvetica', 11, 'bold'), fg="white",
                                      bg="black")
        database_check_salary.place(x=300, y=260)
        database_check_salary_fd = Entry(self.root)
        database_check_salary_fd.place(x=500, y=260)
        if "0" != self.e.sal_check():
            database_check_salary_fd.insert(END, "Connected")
        else:
            database_check_salary_fd.insert(END, "Not connected")

        cloud_b = Button(self.root, text="Upload", width=20, height=2, bg='black', fg='white',
                         font=('Helvetica', 11, 'bold'),
                         command=self.upload_i)
        cloud_b.place(x=0, y=345)
        close = Button(self.root, text="x", font=('Helvetica', 11, 'bold'), command=exit)
        close.place(x=0, y=0)
        download_b = Button(self.root, text="Download", width=20, height=2, bg='black', fg='white',
                            font=('Helvetica', 11, 'bold'),
                            command=self.download)
        download_b.place(x=810, y=210)
        commit = Button(self.root, text="Status", width=20, height=2, bg='black', fg='white',
                        font=('Helvetica', 11, 'bold'),
                        command=employee_manger.full_list_upload_download)
        commit.place(x=810, y=75)

        commit = Button(self.root, text="Activity", width=20, height=2, bg='black', fg='white',
                        font=('Helvetica', 11, 'bold'),
                        command=employee_manger.attendance_cntrl)
        commit.place(x=810, y=300)

        colleague_info = Label(text="GAMA(Limited user) \n(Class implementation,Proctoring,Conflict "
                                    "handling)\nServices used "
                                    ":Cloud(Dropbox)",
                               bg='black', fg='white', font=('Helvetica', 11, 'bold'))
        colleague_info.place(x=310, y=300)
        self.root.mainloop()

    @staticmethod
    def upload_i():
        file.file_interface_upload(0)

    def meeting_id(self):
        root = Tk()
        root.title("Call")
        root.geometry("170x90")
        get_id = Label(root, text="Type your meeting_id", font=('Helvetica', 11, 'bold'))
        get_id_fd = Entry(root)
        get_id_fd.place(x=0, y=30)
        get_id.place(x=10, y=10)

        def give():
            self.c.get_meet_id(get_id_fd.get())

        commit = Button(root, text="CALL", bg='black', fg='white', font=('Helvetica', 11, 'bold'), command=give)
        commit.place(x=50, y=60)

    def site(self):
        if self.site_var.get() == "Set down":
            self.site_var.set("Activate")
        else:
            self.site_var.set("Set down")

    @staticmethod
    def download():
        file.file_interface_download(0)


if __name__ == "__main__":
    interface_3()
