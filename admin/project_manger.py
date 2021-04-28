from tkinter import *
import sqlite3
from admin.cloud_manager import cloud_manger
import os



def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


cloud = cloud_manger()


def sync(i):
    if i == 1:
        cloud.database_sync_get()
    else:
        cloud.database_sync_set()


class project_handel_func:
    def __init__(self):
        self.db = sqlite3.connect(curr_d()+'/admin/oms.db')
        self.cursor = self.db.cursor()

    def reconnect(self):
        self.db = sqlite3.connect(curr_d()+'/admin/oms.db')
        self.cursor = self.db.cursor()

    def get_emp_proj(self, emp_id):
        self.reconnect()
        x = []
        self.cursor.execute("SELECT * FROM project WHERE assign=? AND status=?", (emp_id, "Not Done",))
        records = self.cursor.fetchall()
        for row in records:
            for i in range(len(row)):
                x.append(row[i])
            return x

    # *****************************( SEARCH SECTION )*************************************************** #
    def search_by_emp_id(self, emp_id):
        self.reconnect()
        self.cursor.execute("SELECT * FROM employee Where emp_id=?", (emp_id,))
        for row in self.cursor.fetchall():
            return True
        else:
            return False

    def search_name(self, name):
        self.reconnect()
        self.cursor.execute("SELECT * FROM employee Where name=?", (name,))
        for row in self.cursor.fetchall():
            return True
        else:
            return False

    def search_proj(self, proj_id):
        self.reconnect()
        self.cursor.execute("SELECT * FROM project Where proj_id=?", (proj_id,))
        for row in self.cursor.fetchall():
            return True
        else:
            return False

    def search_proj_name(self, name):
        self.reconnect()
        self.cursor.execute("SELECT * FROM project Where proj_name=?", (name,))
        for row in self.cursor.fetchall():
            return True
        else:
            return False

    # *****************************************( SEARCH END )*************************************** #
    def get_no_of_proj(self):
        self.reconnect()
        i = 0
        self.cursor.execute("SELECT proj_id FROM project")
        for employee in self.cursor:
            for j in range(len(employee)):
                i = i + 1
        return i

    def get_no_of_proj_done(self):
        self.reconnect()
        i = 0
        self.cursor.execute("SELECT proj_id FROM project WHERE status=?", ("Done",))
        for employee in self.cursor:
            for j in range(len(employee)):
                i = i + 1
        return i

    # Update the employee table when project is added
    def update_project(self, project, emp_id):
        self.reconnect()
        self.db.execute("UPDATE employee SET project=? WHERE emp_id=?",
                        (project + 1, emp_id))
        self.db.commit()

    def p_id_get(self):
        self.reconnect()
        i = 0
        self.cursor.execute("SELECT proj_id FROM project ")
        for project in self.cursor:
            for j in range(len(project)):
                if project[0] > i:
                    i = project[0]
        i = str(i + 1)
        return i

    # give complete record of project
    def get_proj_rcrd(self, emp_id):
        self.reconnect()
        x = []
        self.cursor.execute("SELECT * FROM project WHERE assign=?", (emp_id,))
        records = self.cursor.fetchall()
        for row in records:
            for i in row(len(row)):
                x.append(row[i])
            return x

    # search for wether that emp_id exist or not
    def search(self, emp_id):
        self.reconnect()
        self.cursor.execute("SELECT * FROM employee Where emp_id=?", (emp_id,))
        for row in self.cursor.fetchall():
            return True
        else:
            return False

    # Entry of proj
    def proj_table(self, proj_id, proj_name, assign=None, date=None):
        self.reconnect()
        if assign is not None:
            x = None
            self.cursor.execute("SELECT * FROM employee WHERE emp_id=?", (assign,))
            for row in self.cursor.fetchall():
                x = row

            if x is not None:
                if assign is not None or date is not None:
                    self.db.execute("INSERT INTO project(proj_id, proj_name, assign,due ,Status) VALUES(?,?,?,?,?)",
                                    (proj_id, proj_name, assign, date, 'Not Done'))
                    self.db.commit()
                    return 1
                else:
                    return 0
            else:
                return 3

    def get_proj(self, emp_id):
        self.reconnect()
        self.cursor.execute("SELECT * FROM employee WHERE emp_id=?", (emp_id,))
        records = self.cursor.fetchall()
        for row in records:
            return row[2]



# shows Whole proj_list list
class proj_list:
    def __init__(self):
        sync(1)
        root = Tk()
        root.geometry("430x310")
        root.title("emp info")

        db = sqlite3.connect(curr_d()+"/admin/oms.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM project ORDER BY proj_id ASC")
        i = 0
        f = Entry(root, width=10, fg='white', bg='black')
        f.grid(row=0, column=0)
        g = Entry(root, width=10, fg='white', bg='black')
        g.grid(row=0, column=1)
        h = Entry(root, width=10, fg='white', bg='black')
        h.grid(row=0, column=2)
        k = Entry(root, width=10, fg='white', bg='black')
        k.grid(row=0, column=3)
        l = Entry(root, width=10, fg='white', bg='black')
        l.grid(row=0, column=4)
        f.insert(END, "proj_id")
        g.insert(END, "proj_Name")
        h.insert(END, "assign_emp_id")
        k.insert(END, "End date")
        l.insert(END, "Status")
        for project in cursor:
            for j in range(len(project)):
                e = Entry(root, width=10, fg='blue')
                e.grid(row=i + 10, column=j)
                e.insert(END, project[j])
            i = i + 1

        root.mainloop()


class add_new_project:
    def __init__(self):
        self.instance = project_handel_func()
        self.root = Tk()
        self.root.geometry("350x170")
        self.root.minsize(350, 170)
        self.root.maxsize(350, 170)
        self.root.title("ASSIGN PROJECT/PROJECT ADD")
        self.user_val = StringVar()
        # LAYOUT
        self.proj_id_lb = Label(self.root, text="Project id *")
        self.proj_id_lb.place(x=1, y=1)
        self.proj_id = Entry(self.root)
        self.proj_id.place(x=150, y=1)
        self.proj_name = Label(self.root, text="Project Name *")
        self.proj_name.place(x=1, y=30)
        self.proj_name_fd = Entry(self.root)
        self.proj_name_fd.place(x=150, y=30)
        self.proj_assign = Label(self.root, text="Assign emp_id *")
        self.proj_assign.place(x=1, y=60)
        self.proj_assign_fd = Entry(self.root, textvariable=self.user_val)
        self.proj_assign_fd.place(x=150, y=60)
        self.proj_date = Label(self.root, text="Project due Date")
        self.proj_date.place(x=1, y=90)
        self.proj_date_fd = Entry(self.root)
        self.proj_date_fd.place(x=150, y=90)
        self.proj_assign_fd.insert(0, "None")
        self.proj_date_fd.insert(0, "00-00-00")
        self.response = Label(self.root, text="response")
        self.response.place(x=100, y=150)
        self.proj_id.insert(END, self.instance.p_id_get())
        self.proj_id.config(state='readonly')

        def out():
            self.root.destroy()

        self.root.bind('<Return>', self.ok)
        b1 = Button(self.root, text="ok", command=self.ok)
        b1.place(x=100, y=120)
        b2 = Button(self.root, text="Close", command=out)
        b2.place(x=200, y=120)
        add = Button(self.root, text="+", command=add_new_project)
        add.place(x=280, y=120)
        self.root.mainloop()

    # ok function
    def ok(self, event=None):
        if self.instance.search(int(self.proj_assign_fd.get())):
            try:
                sync(1)
                self.instance.update_project(self.instance.get_proj(int(self.proj_assign_fd.get())),
                                             int(self.proj_assign_fd.get()))
                self.instance.proj_table(int(self.proj_id.get()), self.proj_name_fd.get(),
                                         int(self.proj_assign_fd.get()),
                                         self.proj_date_fd.get())
                self.response.config(text="Successfully Done")
                sync(0)
            except Exception as error:
                self.response.config(text=error)
        else:
            self.response.config(text="emp_id not Available")
