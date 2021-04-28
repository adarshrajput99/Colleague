import admin.cloud_manager
import os
import admin.conflict_manger


def curr_d():
    x = os.path.split(os.getcwd())
    return x[0]


def conflict_handler(text, emp_id):
    c = admin.cloud_manager.cloud_manger()
    print("/home/adarshsingh/stats/" + str(emp_id))
    c.download_stats("/home/adarshsingh/stats/" + str(emp_id))
    admin.conflict_manger.write_logs(text)
    try:
        c.upload(curr_d() + "/Logs/stats", "/home/adarshsingh/stats/" + str(emp_id))
    except Exception as e:
        c.del_stats(emp_id)
        c.upload(curr_d() + "/Logs/stats", "/home/adarshsingh/stats/" + str(emp_id))
