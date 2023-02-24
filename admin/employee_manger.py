from tkinter import *
import sqlite3
from datetime import date

from admin.project_manger import project_handel_func
from admin.cloud_manager import cloud_manger
import os


def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


cloud = cloud_manger()


# a_30_10_2020_22_48_23_22_47_56_
# 0123456789012345678901234567890

def decoder(x):
    attendance = ""
    start_time = ""
    end_time = ""
    date = ""
    if x[0] == "p":
        attendance = "present"
    else:
        attendance = "Absent"

    for i in range(22, 30, 1):
        if x[i] != "_":
            start_time = start_time + x[i]
        else:
            start_time = start_time + ":"
    for i in range(13, 21, 1):
        if x[i] != "_":
            end_time = end_time + x[i]
        else:
            end_time = end_time + ":"
    for i in range(2, 12, 1):
        if x[i] != "_":
            date = date + x[i]
        else:
            date = date + "/"
    return [attendance, start_time, end_time, date]


def time_diff_calc(start, end):
    def sec_calc(x):
        hour = x[0] + x[1]
        minute = x[3] + x[4]
        sec = x[6] + x[7]
        return int(hour) * 3600 + int(minute) * 60 + int(sec)

    if sec_calc(end) > sec_calc(start):
        total_time = sec_calc(end) - sec_calc(start)
    else:
        total_time = (86400 - sec_calc(start)) + sec_calc(end)

    def hour_conv(x):
        hour = int(x / 3600)
        minute = int((x % 3600) / 60)
        sec = (x % 3600) % 60
        if sec == 0:
            sec = str(sec) + "0"
        if hour == 0:
            hour = str(hour) + "0"
        if minute == 0:
            minute = str(minute) + "0"
        return str(hour) + ":" + str(minute) + ":" + str(sec)

    return hour_conv(total_time)


def sync(i):
    if i == 1:
        cloud.database_sync_get()
    else:
        cloud.database_sync_set()


# ****************************************** Manage all employee *******************************************************
class emp_manage_functions:
    def __init__(self):
        self.db = sqlite3.connect(curr_d() + '/admin/oms.db')
        self.cursor = self.db.cursor()
        self.p = project_handel_func()
        self.c = cloud_manger()

    def re_connect(self):
        self.db = sqlite3.connect(curr_d() + '/admin/oms.db')
        self.cursor = self.db.cursor()

    def mark_myProject_Done(self, emp_id):
        self.c.database_sync_get()
        self.re_connect()
        db = sqlite3.connect(curr_d() + '/admin/oms.db')
        if self.p.search_by_emp_id(emp_id):
            db.execute("UPDATE project SET status=? WHERE assign=?", ("Done", emp_id,))
            db.commit()
        self.c.database_sync_set()

    def sal_check(self):
        self.re_connect()
        i = 0
        self.cursor.execute("SELECT grade FROM salary ")
        for employee in self.cursor:
            for j in range(len(employee)):
                i = i + 1
        return i

    # changes the feedback
    def feedback_change(self, feedback, emp_id):
        self.re_connect()
        print(feedback, emp_id, type(feedback), type(emp_id))
        print(self.db.execute("UPDATE employee SET feedback=? WHERE emp_id=?",
                              (feedback, emp_id,)))
        print(self.db.commit())

    # last change get
    def last_change(self, emp_id):
        x = self.get_download_line(emp_id)
        y = ""
        last = ""
        z = len(x) - 1
        for i in range(z, 0, -1):
            if x[i] == "{":
                break
            else:
                y = y + x[i]
        for i in range(len(y) - 1, -1, -1):
            last = last + y[i]
        return last

    # Returns the last employee added
    def get_last_emp_added(self, ):
        self.re_connect()
        i = 0
        self.cursor.execute("SELECT emp_id FROM employee ORDER BY grade DESC")
        for employee in self.cursor:
            for j in range(len(employee)):
                if employee[0] > i:
                    i = employee[0]
        # self.db.close()
        return i

    # Adds the employee
    def add_emp(self, emp_id, name, project, grade):
        self.re_connect()
        join_date = date.today()
        emp_id = int(emp_id)
        project = int(project)
        grade = int(grade)
        self.db.execute(
            "INSERT INTO employee(emp_id,name,project,grade,join_date,commit_length,commits,feedback) VALUES(?,?,"
            "?,?,?,0,?,?)",
            (emp_id, name, project, grade, join_date, "/start", "no feedback"))
        self.db.commit()
        # self.db.close()

    # Sets the grade of employee
    def change_grade(self, emp_id, name, project, grade):
        self.re_connect()
        self.db.execute("UPDATE employee SET emp_id=?,name=?,project=?,grade=? WHERE emp_id=?",
                        (emp_id, name, project, grade, emp_id))
        self.db.commit()
        # self.db.close()

    # Return whole record of employee------->Format[emp_id,name,project,grade,join_date,commit,commit_length,Feedback]
    def get_full_emp_record(self, emp_id):
        self.re_connect()
        x = []
        self.cursor.execute("SELECT * FROM employee WHERE emp_id=?", (emp_id,))
        records = self.cursor.fetchall()
        for row in records:
            for i in range(len(row)):
                x.append(row[i])
            return x
        # self.db.close()

    # Update the record of employee
    def update_record_emp(self, emp_id, name, project, grade):
        self.re_connect()
        self.db.execute("UPDATE employee SET name=?,project=?,grade=? WHERE emp_id=?",
                        (name, project, grade, emp_id))
        self.db.commit()
        # self.db.close()

    # Delete the emp record
    def delete_emp(self, emp_id):
        self.re_connect()
        self.cursor.execute("DELETE FROM employee WHERE emp_id=?", (emp_id,))
        self.db.commit()
        # self.db.close()

    # It returns the list in a single line
    def get_download_line(self, emp_id):
        return self.c.get_read_stats(emp_id)

    # It converts it in row format(as a list)
    def commit_conversion_row(self, emp_id):
        self.re_connect()
        x = self.get_download_line(emp_id)
        y = ""
        for i in range(len(x)):
            if x[i] == "#":
                y = y + "\n"
            y = y + x[i]
        return y

    # Get no of commits
    def get_no_commits(self, emp_id):
        self.re_connect()
        emp_id = int(emp_id)
        self.cursor.execute("SELECT commit_length FROM employee WHERE emp_id=?", (emp_id,))
        for employee in self.cursor:
            self.db.close()
            return employee[0]

    # Get salary--------->Format[Start_Range,End_Range]
    def sal_get(self, emp_id):
        self.re_connect()

        def grade_conv(temp):
            grade = 0
            if 11 > temp > 0:
                grade = 1
            elif 10 < temp < 21:
                grade = 2
            elif 20 < temp < 31:
                grade = 3
            elif 30 < temp < 41:
                grade = 4
            elif 40 < temp < 51:
                grade = 5
            elif 50 < temp < 61:
                grade = 6
            return grade

        grade_emp = -1
        sal = []
        self.cursor.execute("SELECT grade FROM employee WHERE emp_id=?", (emp_id,))
        records = self.cursor.fetchall()
        for row in records:
            grade_emp = row[0]
        grade_sal = grade_conv(grade_emp)
        self.cursor.execute("SELECT * FROM salary WHERE grade=?", (grade_sal,))
        records = self.cursor.fetchall()
        for row in records:
            for i in range(len(row)):
                sal.append(row[i])
        return sal

    def write(self, text, emp_id):
        self.re_connect()
        x = self.get_download(emp_id) + text
        self.db.execute("UPDATE employee SET commits=?,commit_length=commit_length+1 WHERE emp_id=?",
                        (x, emp_id))
        self.db.commit()

    def get_download(self, emp_id):
        self.re_connect()
        self.cursor.execute("SELECT commits FROM employee WHERE emp_id=?", (emp_id,))
        for employee in self.cursor:
            return employee[0]

    def get_no_of_emp(self):
        self.re_connect()
        i = 0
        self.cursor.execute("SELECT emp_id FROM employee ORDER BY grade DESC")
        for employee in self.cursor:
            for j in range(len(employee)):
                i = i + 1
        return i

    def create_pass(self, emp_id, key):
        import admin.interface2
        self.re_connect()
        self.db.execute(
            "INSERT INTO pass(emp_id,key) VALUES(?,?)",(emp_id, admin.interface2.encrypt(key)))
        self.db.commit()


# ****************************************** Emp performance set(Completely working)************************************
class emp_performance_set:
    def __init__(self):
        sync(1)
        self.p = emp_manage_functions()
        self.root = Tk()
        self.root.geometry("350x170")
        self.root.minsize(350, 170)
        self.root.maxsize(350, 170)
        self.root.title(" EMPLOYEE PERFORMANCE")

        # LAYOUT
        self.emp_id_lb = Label(self.root, text="User id *")
        self.emp_id_lb.place(x=1, y=1)
        self.emp_id = Entry(self.root)
        self.emp_id.place(x=150, y=1)
        self.emp_name = Label(self.root, text="Admin Name *")
        self.emp_name.place(x=1, y=30)
        self.emp_name_fd = Entry(self.root)
        self.emp_name_fd.place(x=150, y=30)
        self.emp_project = Label(self.root, text="No of room")
        self.emp_project.place(x=1, y=60)
        self.emp_project_fd = Entry(self.root)
        self.emp_project_fd.place(x=150, y=60)
        self.emp_grade = Label(self.root, text="Capacity ")
        self.emp_grade.place(x=1, y=90)
        self.emp_grade_fd = Entry(self.root)
        self.emp_grade_fd.place(x=150, y=90)
        self.emp_project_fd.insert(0, "0")
        self.emp_grade_fd.insert(0, "0")
        self.response = Label(self.root)
        self.response.place(x=100, y=150)
        self.b1 = Button(self.root, text="Get", command=self.get)
        self.b1.place(x=100, y=120)
        self.b2 = Button(self.root, text="Close", command=self.out)
        self.b2.place(x=200, y=120)
        self.b3 = Button(self.root, text="ok", command=self.ok)
        self.b3.place(x=30, y=120)
        self.root.bind('<Return>', self.get)
        self.root.mainloop()

    def get(self, event=None):
        row = self.p.get_full_emp_record(int(self.emp_id.get()))
        self.emp_name_fd.insert(END, row[1])
        self.emp_project_fd.insert(END, row[2])
        self.emp_grade_fd.insert(END, row[3])

    def ok(self):
        sync(1)
        if self.emp_name_fd.get() == "":
            self.response.config(text="Name field could not be empty")
        else:
            try:
                self.p.update_record_emp(int(self.emp_id.get()), self.emp_name_fd.get(), int(self.emp_project_fd.get()),
                                         int(self.emp_grade_fd.get()))
                self.response.config(text="operation Successful ")
                sync(0)
            except Exception as e:
                print(e)
                self.response.config(text="*****")

    def out(self):
        self.root.destroy()


# ****************************************** Add emp(Completely working) ***********************************************
class add_emp:
    def __init__(self):
        sync(1)
        self.p = emp_manage_functions()
        self.cloud = cloud_manger()
        self.root = Tk()
        self.root.geometry("350x170")
        self.root.minsize(350, 170)
        self.root.maxsize(350, 170)
        self.root.title("ADD EMPLOYEE")

        # LAYOUT
        self.emp_id_lb = Label(self.root, text="Employee id *")
        self.emp_id_lb.place(x=1, y=1)
        self.emp_id = Entry(self.root)
        self.emp_id.place(x=150, y=1)
        self.emp_name = Label(self.root, text="Employee Name *")
        self.emp_name.place(x=1, y=30)
        self.emp_name_fd = Entry(self.root)
        self.emp_name_fd.place(x=150, y=30)
        self.emp_project = Label(self.root, text="Employee Password")
        self.emp_project.place(x=1, y=60)
        self.emp_project_fd = Entry(self.root)
        self.emp_project_fd.place(x=150, y=60)
        self.emp_grade = Label(self.root, text="Employee Grade ")
        self.emp_grade.place(x=1, y=90)
        self.emp_grade_fd = Entry(self.root)
        self.emp_grade_fd.place(x=150, y=90)
        self.emp_project_fd.insert(0, "Password")
        self.emp_grade_fd.insert(0, "0")
        self.response = Label(self.root)
        self.response.place(x=100, y=150)
        self.emp_id.insert(END, self.p.get_last_emp_added() + 1)
        self.emp_id.config(state='readonly')
        self.root.bind('<Return>', self.ok)
        self.b1 = Button(self.root, text="ok", command=self.ok)
        self.b1.place(x=100, y=120)
        self.b2 = Button(self.root, text="Close", command=self.close)
        self.b2.place(x=200, y=120)

        self.root.mainloop()

    # ok function
    def ok(self, event=None):
        sync(1)
        self.p.add_emp(self.emp_id.get(), self.emp_name_fd.get(), "0",
                       self.emp_grade_fd.get())
        self.p.create_pass(self.emp_id.get(),self.emp_project_fd.get())
        try:
            self.cloud.make_folder(self.emp_id.get())
            self.cloud.make_attendence(self.emp_id.get())
            self.cloud.make_image(self.emp_id.get())
            sync(0)
        except Exception as e:
            print(e)
        self.response.config(text="Entry Successful")
        self.root.destroy()
        add_emp()

    def close(self):
        self.root.destroy()


# ****************************************** Shows full database(Completely working) ***********************************
class complete_emp_list:
    def __init__(self):
        sync(1)
        root = Tk()
        root.geometry("602x400")
        root.title("Emp List")

        db = sqlite3.connect(curr_d() + "/admin/oms.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employee ORDER BY grade DESC")
        i = 0
        f = Entry(root, width=10, fg='white', bg='black')
        f.grid(row=0, column=0)
        g = Entry(root, width=10, fg='white', bg='black')
        g.grid(row=0, column=1)
        h = Entry(root, width=10, fg='white', bg='black')
        h.grid(row=0, column=2)
        k = Entry(root, width=10, fg='white', bg='black')
        l = Entry(root, width=10, fg='white', bg='black')
        m = Entry(root, width=10, fg='white', bg='black')
        n = Entry(root, width=10, fg='white', bg='black')
        l.grid(row=0, column=4)
        k.grid(row=0, column=3)
        m.grid(row=0, column=5)
        n.grid(row=0, column=6)
        m.insert(END, "Activity")
        n.insert(END, "Activity_no")
        f.insert(END, "USER-ID")
        g.insert(END, "ADMIN")
        h.insert(END, "ROOM")
        k.insert(END, "LIMIT")
        l.insert(END, "Join_Date")
        for employee in cursor:
            for j in range(len(employee)):
                e = Entry(root, width=10, fg='blue')
                e.grid(row=i + 10, column=j)
                e.insert(END, employee[j])
            i = i + 1

        root.mainloop()


# ****************************************** Del emp(Completely working) ***********************************************
class del_emp:
    def __init__(self):
        sync(1)
        self.p = emp_manage_functions()
        self.client = cloud_manger()
        self.root = Tk()
        self.root.geometry("300x100")
        self.root.minsize(300, 100)
        self.root.maxsize(300, 100)
        self.root.title("REMOVE EMPLOYEE")

        # LAYOUT
        self.delete_lab = Label(self.root, text="ENTER EMP_ID")
        self.delete_lab.place(x=1, y=1)
        self.delete_fd = Entry(self.root)
        self.delete_fd.place(x=120, y=1)
        self.delete_bt = Button(self.root, text="Delete", command=self.delete_h)
        self.delete_bt.place(x=60, y=30)
        self.delete_cancel = Button(self.root, text="cancel", command=self.out)
        self.delete_cancel.place(x=150, y=30)
        self.delete_response = Label(self.root, text="!!Check before deleting")
        self.delete_response.place(x=60, y=70)
        self.root.bind('<Return>', self.delete_h)
        self.root.mainloop()

    def delete_h(self, event=None):
        try:
            sync(1)
            self.p.delete_emp(int(self.delete_fd.get()))
            self.client.remove_folder(self.delete_fd.get())
            self.delete_response.config(text="successfully deleted")
            sync(0)
            self.root.destroy()

        except Exception as e:
            print(e)
            self.delete_response.config(text="error!!!")

    def out(self):
        self.root.destroy()


# ****************************************** Shows the list of upload and download *************************************
class full_list_upload_download:
    def __init__(self):
        sync(1)
        self.p = emp_manage_functions()
        self.root = Tk()
        self.root.geometry("580x450")
        self.root.title("EMPLOYEE UPDATES")
        self.no_lb = Label(self.root, text="NUMBER OF COMMITS :")
        self.no_lb.place(x=0, y=6)
        self.no = Entry(self.root)
        self.no.place(width=35)
        self.emp_id = Label(self.root, text="EMP_ID:")
        self.emp_id.place(x=200, y=6)
        self.commits_fd = Text(self.root)
        self.emp_id_fd = Entry(self.root)
        self.emp_id_fd.place(x=260, y=5)
        self.commits = Label(self.root, text="COMMITS:-", anchor="center")
        self.commits.place(x=0, y=30)
        self.no.place(x=165, y=5)
        self.get_b = Button(self.root, text="GET", command=self.get, width=10)
        self.get_b.place(x=430, y=0)
        self.root.mainloop()

    def get(self):
        self.commits_fd.place(x=0, y=60)
        try:
            self.commits_fd.insert(END, self.p.commit_conversion_row(self.emp_id_fd.get()))
        except Exception as e:
            print(e)
        self.no.insert(END, str(self.p.get_no_commits(self.emp_id_fd.get())))


class feedback:
    def __init__(self):
        sync(1)
        self.p = emp_manage_functions()
        self.root = Tk()
        self.root.geometry("450x210")
        self.root.title("EMPLOYEE FEEDBACK")
        self.emp_id_lb = Label(self.root, text="Emp_id*     :")
        self.emp_id_lb.place(x=0, y=2)
        self.emp_id = Entry(self.root)
        self.emp_id.place(x=90, y=0)
        self.emp_id_grade = Label(self.root, text="Emp_grade :")
        self.emp_id_grade.place(x=0, y=30)
        self.emp_id_grade_fd = Entry(self.root)
        self.emp_id_grade_fd.place(x=90, y=30)
        self.emp_id_name_lb = Label(self.root, text="Emp_name :")
        self.emp_id_name_lb.place(x=0, y=60)
        self.emp_id_name = Entry(self.root)
        self.emp_id_name.place(x=90, y=60)
        self.emp_project = Label(self.root, text="Project        :")
        self.emp_project.place(x=0, y=90)
        self.emp_project_fd = Entry(self.root)
        self.emp_project_fd.place(x=90, y=90)
        self.last_file = Label(self.root, text="Last file      :-")
        self.last_file.place(x=0, y=120)
        self.last_file_fd = Entry(self.root)
        self.last_file_fd.place(width=265)
        self.last_file_fd.place(x=0, y=140)

        self.get = Button(self.root, text="Get", width=10, command=self.set)
        self.get.place(x=4, y=170)
        self.line_vertical = Label(self.root, text="|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n|\n")
        self.line_vertical.place(x=260, y=0)
        self.feedback_fd = Text(self.root)
        self.feedback_fd.place(x=270)
        self.feedback_fd.place(height=200, width=178)
        self.get_change = Button(self.root, text="Give", width=10, command=self.give)
        self.get_change.place(x=120, y=170)
        self.feedback_fd.insert(END, "Type your feedback")

        self.root.mainloop()

    def emp_set(self):
        db = sqlite3.connect(curr_d() + '/admin/oms.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employee WHERE emp_id=?", (self.emp_id.get(),))
        records = cursor.fetchall()
        for row in records:
            self.emp_id_grade_fd.insert(END, row[3])
            self.emp_id_name.insert(END, row[1])
            self.emp_project_fd.insert(END, row[2])
        db.close()

    def set(self):
        sync(1)
        self.last_file_fd.insert(END, self.p.last_change(self.emp_id.get()))
        self.emp_set()

    def give(self):
        sync(1)
        self.p.feedback_change(self.feedback_fd.get('1.0', END), int(self.emp_id.get()))
        sync(0)


class attendance_cntrl:
    def __init__(self):
        self.p = emp_manage_functions()
        self.root = Tk()
        self.client = cloud_manger()
        self.root.geometry("800x410")
        self.root.title("EMPLOYEE UPDATES")
        self.emp_id = Label(self.root, text="EMP_ID:")
        self.emp_id.place(x=0, y=6)
        self.commits_fd = Text(self.root)
        self.emp_id_fd = Entry(self.root)
        self.emp_id_fd.place(x=60, y=5)
        self.commits_fd.place(width=798)
        self.commits_fd.place(x=0, y=40)
        self.get_b = Button(self.root, text="GET", command=self.get, width=10)
        self.get_b.place(x=240, y=3)
        self.root.mainloop()

    def get(self):
        x = self.client.get_attendance(self.emp_id_fd.get())
        for i in x:
            if i == self.emp_id_fd.get():
                continue
            split = decoder(i)
            # [attendance, start_time, end_time, date]
            self.commits_fd.insert('1.0', "Date:" + split[3] + "  Start time:" + split[1] + "  End time:" + split[
                2] + "  Total time:" + time_diff_calc(split[1], split[2]) + " Attendance Report:" + split[0] + "\n")


if __name__ == "__main__":
    x = attendance_cntrl()
