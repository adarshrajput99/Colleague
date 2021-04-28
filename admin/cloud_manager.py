import dropbox
from admin.conflict_manger import *
import os


def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


# Manges all cloud operation
class cloud_manger:

    def __init__(self):
        self.token = 'eM8QnMm92mUAAAAAAAAAAd7WgRgIsLb2tDIoCi4k9dbhejOSuobCUEC8m3k_AiAz'
        try:
            self.client = dropbox.Dropbox(self.token)
            print("link done")
        except Exception as e:
            print(e)

        try:
            self.dbx = dropbox.Dropbox(self.token)

        except Exception as e:
            print(e)

    def get_read_stats(self, emp_id):
        try:
            print(
                self.dbx.files_download_to_file(curr_d() + "/Logs/stats",
                                                path="/home/adarshsingh/stats/" + str(emp_id),
                                                rev=None))
            with open(curr_d() + '/Logs/stats', 'r+') as my_file:
                return my_file.read()
        except Exception as e:
            return  " No Data"

    # returns the number of available files to download(Temporary)
    def search(self):
        x = []
        result = self.dbx.files_list_folder("/home/adarshsingh/user_file/", recursive=True)
        file_list = []

        def process_entries(entries):
            for entry in entries:
                file_list.append([entry.name])

        process_entries(result.entries)
        while result.has_more:
            result = self.dbx.files_list_folder_continue(result.cursor)

            process_entries(result.entries)
        check = False

        for i in file_list:
            for y in i:
                if y != "Mail" and y != "user_file":
                    x.append(y)

        return x

    def make_folder(self, emp_id):
        try:
            print(self.dbx.files_create_folder("/home/adarshsingh/mail/" + str(emp_id)))
        except Exception as e:
            self.client.files_delete("/home/adarshsingh/mail/" + str(emp_id))
            print(self.dbx.files_create_folder("/home/adarshsingh/mail/" + str(emp_id)))

    def make_attendence(self, emp_id):
        try:
            print(self.dbx.files_create_folder("/home/adarshsingh/attendance/" + str(emp_id)))
        except Exception as e:
            self.client.files_delete("/home/adarshsingh/attendance/" + str(emp_id))
            print(self.dbx.files_create_folder("/home/adarshsingh/attendance/" + str(emp_id)))

    def make_image(self, emp_id):
        try:
            print(self.dbx.files_create_folder("/home/adarshsingh/attendance/" + str(emp_id) + "/image_pile"))
        except Exception as e:
            self.client.files_delete("/home/adarshsingh/attendance/" + str(emp_id) + "/image_pile")
            print(self.dbx.files_create_folder("/home/adarshsingh/attendance/" + str(emp_id) + "/image_pile"))

    def remove_folder(self, emp_id):
        self.client.files_delete("/home/adarshsingh/mail/" + str(emp_id))
        self.client.files_delete("/home/adarshsingh/" + str(emp_id))
        pass

    def search_mail(self, emp_id):
        x = []
        result = self.dbx.files_list_folder("/home/adarshsingh/mail/" + str(emp_id) + "/", recursive=True)

        file_list = []

        def process_entries(entries):
            for entry in entries:
                file_list.append([entry.name])

        process_entries(result.entries)
        while result.has_more:
            result = self.dbx.files_list_folder_continue(result.cursor)
            process_entries(result.entries)

        for i in file_list:
            for y in i:
                if y != "Mail":
                    x.append(y)

        return x

    def search_image(self, emp_id):
        x = []
        result = self.dbx.files_list_folder("/home/adarshsingh/attendance/" + str(emp_id) + "/image_pile/",
                                            recursive=True)

        file_list = []

        def process_entries(entries):
            for entry in entries:
                file_list.append([entry.name])

        process_entries(result.entries)
        while result.has_more:
            result = self.dbx.files_list_folder_continue(result.cursor)
            process_entries(result.entries)

        for i in file_list:
            for y in i:
                if y != "Mail":
                    x.append(y)

        return x

    def get_attendance(self, emp_id):
        x = []
        result = self.dbx.files_list_folder("/home/adarshsingh/attendance/" + str(emp_id) + "/",
                                            recursive=True)

        file_list = []

        def process_entries(entries):
            for entry in entries:
                file_list.append([entry.name])

        process_entries(result.entries)
        while result.has_more:
            result = self.dbx.files_list_folder_continue(result.cursor)
            process_entries(result.entries)

        for i in file_list:
            for y in i:
                if y != "image_pile":
                    x.append(y)

        return x

    def available_files(self):
        x = []
        list = self.search()
        for i in range(len(list)):
            x.append(list[i])
        return x

    def mail(self, emp_id):
        self.emp_id_mail = emp_id
        x = self.search_mail(emp_id)
        for i in x:
            if i == str(emp_id):
                return True
            else:
                return False

    def mail_getter(self, emp_id):
        x = self.search_mail(emp_id)

        if len(x) != 1:
            for i in range(1, len(x)):
                print(x[i])

                print(self.dbx.files_download_to_file(
                    curr_d() + "/Logs/mail/" + str(x[i]),
                    path="/home/adarshsingh/mail/" + str(emp_id) + "/" + str(x[i]),
                    rev=None))
                print("done")

    def file_uploader(self, emp_id, sender_emp_id):
        x = self.search_mail(emp_id)
        mail_found = 0
        for y in range(0, 9):
            for mails in x:
                if str(mails) == str(sender_emp_id) + "_" + str(y):
                    print("condition match")
                    mail_found = mail_found + 1
        print(self.upload(curr_d() + "/Logs/mail_send/mail_temp", "/home"
                                                                  "/adarshsingh"
                                                                  "/mail/" + str(
            emp_id) + "/" + str(sender_emp_id) + "_" + str(mail_found + 1)))

    # UPLOADING A FILE
    def upload(self, file_path, dbx_path=""):

        def get_file_name(x):
            rev_path = ""
            name = ""
            for i in range(len(x) - 1, 0, -1):
                if x[i] != "/":
                    rev_path = rev_path + x[i]
                else:
                    break
            for i in range(len(rev_path) - 1, -1, -1):
                name = name + rev_path[i]
            return name

        if dbx_path != "":
            self.client.files_upload(open(file_path, "rb").read(), dbx_path)
        else:
            dbx_path = "/home/adarshsingh/user_file/" + get_file_name(file_path)
            self.client.files_upload(open(file_path, "rb").read(), dbx_path)

    # searching a file
    def search_single_file(self, file_name):
        x = []
        x = file_name
        result = self.dbx.files_list_folder("", recursive=True)
        file_list = []

        def process_entries(entries):
            for entry in entries:
                file_list.append([entry.name])

        process_entries(result.entries)

        while result.has_more:
            result = self.dbx.files_list_folder_continue(result.cursor)

            process_entries(result.entries)
        check = False
        for i in file_list:
            for y in i:
                if x == y:
                    return True
        else:
            return False

    def download_stats(self, dbx_path):
        print(
            self.dbx.files_download_to_file(curr_d() + "/Logs/stats",
                                            path=dbx_path,
                                            rev=None))
        print("done")

    # download files selected by user
    def download(self, file, path="/home/adarshsingh/user_file/"):
        print(
            self.dbx.files_download_to_file(os.path.expanduser("~") + "/Downloads/" + file,
                                            path=path + file,
                                            rev=None))
        print("done")

    def del_stats(self, emp_id):
        self.client.files_delete("/home/adarshsingh/stats/" + str(emp_id))

    def get_meet_id(self, meeting_id):
        print(
            self.dbx.files_download_to_file(curr_d() + "/Logs/meeting_link",
                                            path="/home/adarshsingh/meeting_id/meeting_link",
                                            rev=None))

        def write_logs(text):
            with open(curr_d() + '/Logs/meeting_link', 'r+') as my_file:
                my_file.write(text)

        try:
            print(self.client.files_delete("/home/adarshsingh/meeting_id/meeting_link"))
        except Exception as e:
            print(e)

        write_logs(meeting_id)

        self.upload(curr_d() + "/Logs/meeting_link", "/home/adarshsingh/meeting_id/meeting_link")

    def retrive_meet_id(self):
        print(
            self.dbx.files_download_to_file(curr_d() + "/Logs/meeting_link",
                                            path="/home/adarshsingh/meeting_id/meeting_link",
                                            rev=None))
        with open(curr_d() + '/Logs/meeting_link', 'r+') as my_file:
            return my_file.read()

    # Download the database
    def database_sync_get(self):
        try:
            os.remove(curr_d() + "/admin/oms.db")
        except Exception as e:
            print(e)
        write_logs("download_state")
        print("Getting database")
        try:
            print(self.dbx.files_download_to_file(curr_d() + "/admin/oms.db",
                                                  path="/home/adarshsingh"
                                                       "/database/oms.db",
                                                  rev=None))
        except Exception as e:
            print(e)
            # self.database_sync_get()
            # print("Connection Time Out")
            # return True

    # Upload the database
    def database_sync_set(self):

        write_logs("No_download_State")
        print("Setting database")
        try:
            print(
                self.upload(curr_d() + "/admin/oms.db",
                            "/home/adarshsingh/database/oms.db"))
        except Exception as e:
            try:
                print(self.client.files_delete("/home/adarshsingh/database/oms.db"))
                print(self.upload(curr_d() + "/admin/oms.db",
                                  "/home/adarshsingh/database/oms.db"))
            except Exception as e:
                # self.database_sync_set()
                print("Connection Time Out")
        os.remove(curr_d() + "/admin/oms.db")

    def remover(self, x):
        for i in self.search_image(x):
            print(self.client.files_delete("/home/adarshsingh/attendance/" + str(x) + "/image_pile/" + i))
