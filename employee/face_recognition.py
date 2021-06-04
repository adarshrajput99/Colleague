import glob
import shutil

import cv2
from datetime import datetime
import time
import employee.user_start_4
from threading import *
import webbrowser
import admin.cloud_manager
import admin.employee_manger
import pyautogui
import os


def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


def take_screen_shot(x):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(curr_d() + '/sr/' + x)


time_start = ""
curr_emp_id = 0


# yes = face not present
# no = face not present

def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


class face_recognition(Thread):
    def stop(self):
        self.stopper = True
        return

    def run(self):
        s = datetime.now()
        self.Start = s.strftime("_%H_%M_%S_")
        self.stopper = False
        prev = []
        face_cascade = cv2.CascadeClassifier(curr_d() + '/employee/haarcascade_frontalface_default.xml')
        x = []
        y = []
        self.no = 0
        self.yes = 0
        cap = cv2.VideoCapture(0)
        mills1 = 0
        mills = 0
        while True:
            if self.stopper:
                break
            _, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                check = (cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2))
                mills1 = int(round(time.time() * 1000))
                self.no = self.no + 1

            else:
                mills = int(round(time.time() * 1000))
                if mills1 != mills:
                    prev.append(mills)
                    self.yes = self.yes + 1
                    if len(prev) == 50:
                        print("condition match")
                        now = datetime.now()
                        my_file = open(curr_d() + "/Logs/temp_logs_face", 'w')
                        my_file.write(now.strftime("%H:%M:%S") + "\n")
                        # take_screen_shot(now.strftime("%H_%M_%S") + ".jpg")
                        prev = []
                cv2.imshow('img', img)
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    print(str(self.yes) + "/" + str(self.no))

                    break


class user_caller(Thread):
    def get_emp_id(self, emp_id):
        self.emp_id = emp_id

    def run(self):
        try:
            employee.user_start_4.user_start(self.emp_id)
        except Exception as e:
            print(e)


th = face_recognition()
th2 = user_caller()


def starter(emp_id):
    th2.get_emp_id(emp_id)
    th.start()
    th2.start()
    x = admin.cloud_manager.cloud_manger()
    webbrowser.open('https://meet.google.com/' + x.retrive_meet_id(), new=2)


def submit_report(emp_id):
    time_start = th.Start
    t = time.strftime('_%d_%m_%Y_%H_%M_%S' + time_start, time.localtime())
    fn = admin.cloud_manager.cloud_manger()
    print(t)
    if th.yes > th.no:
        t = "a" + t
        print("ABSENT")
        print(fn.upload(curr_d() + "/Logs/temp_logs_face", "/home/adarshsingh/attendance/" + emp_id + "/" + t))
        try:
            fn.remover(emp_id)
        except Exception as e:
            print(e)
        for file_get in glob.glob("*"):
            os.remove(curr_d() + '/Logs/mail/' + str(file_get))
        try:
            shutil.rmtree(curr_d() + "/sr/")
        except Exception as e:
            print(e)
        os.mkdir(curr_d() + "/sr/")
    else:
        t = "p" + t
        print(fn.upload(curr_d() + "/Logs/temp_logs_face", "/home/adarshsingh/attendance/" + str(emp_id) + "/" + t))
        print("PRESENT")
        try:
            shutil.rmtree(curr_d() + "/sr/")
        except Exception as e:
            print(e)
        os.mkdir(curr_d() + "/sr/")


def stop(emp_id):
    try:
        th.stop()
        submit_report(emp_id)
        print(str(th.yes) + "/" + str(th.no))
    except Exception as e:
        print(e)
