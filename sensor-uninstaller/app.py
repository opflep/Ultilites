import time

import requests
import schedule

from githubalert import GithubAlert

sentry_sdk.init("http://9c2928bbf07040739e6ad3f76935ddd4@10.14.132.113:9000/3")


def job():
    try:
        message = ''
        status = True
        GithubAlert().run()
        requests.post(crontab_url, headers={
            'Content-Type': 'application/json',
        }, data='{"task_name":"github-alert-daily-' + str(interval_hour) + '"}')

    except Exception as e:
        message = str(e)
        status = False
        try:
            requests.post('http://10.14.132.39:24021/verify_crontab', headers={
                'Content-Type': 'application/json',
            }, data='{"task_name":"github-alert-exception"}')
        except:
            pass
    logger.info('{} : {} : {}'.format('github-alert', status, message))


# run first job
job()
# then execute by schedule later
schedule.every(interval_hour).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
