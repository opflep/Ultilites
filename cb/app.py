import time

import json
import requests
import schedule

from carbonblack import CarbonBlackClient
from config import Config


def job():
    try:
        cb = CarbonBlackClient()
        if (cb.sensors_count_by_group()['agent']['total'] > 10):
            sensors = cb.get_sensors_bygroup()
            cb.uninstallExceededSensor(sensors)

    except Exception as e:
        message = str(e)
        print(message)

    # print(response.text.encode('utf8'))
    
# run first job
job()
# then execute by schedule later
schedule.every(3).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


# if __name__ == "__main__":
#     job()