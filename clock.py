# from apscheduler.schedulers.blocking import BlockingScheduler
# import urllib.request
# from urllib.request import urlopen

# sched = BlockingScheduler()

# @sched.scheduled_job('cron', minute='*/20')
# def scheduled_job():
#     url = "https://stockbottttt.herokuapp.com/"
#     conn = urllib.request.urlopen(url)
        
#     for key, value in conn.getheaders():
#         print(key, value)

# sched.start()