import os
# import re
import json
import requests
import jsonpickle

# import cbapi
from cbapi import CbResponseAPI
from cbapi.response import SensorGroup, Sensor, Alert, Watchlist, Feed
from config import Config
# from .config import Config
class Endpoint:

    def __init__(self, computer_name, dns_name, last_checkin_time, network_interfaces, os, status):
        self.computer_name = computer_name
        self.dns_name = dns_name
        self.last_checkin_time = last_checkin_time
        self.network_interfaces = network_interfaces
        self.os = os
        self.status = status

# class Alert_json:

#     def __init__(self, hostname, dns_name, last_checkin_time, network_interfaces, os, status):
#         self.hostname = hostname
#         self.dns_name = dns_name
#         self.last_checkin_time = last_checkin_time
#         self.network_interfaces = network_interfaces
#         self.os = os
#         self.status = status

class CarbonBlackClient:

    def __init__(self):
        os.environ['CBAPI_URL'] = 'https://10.14.132.35'
        os.environ['CBAPI_TOKEN'] = 'ffe48bcb6caa1d91a988d512a4b707e66d9dd9ff'
        os.environ['CBAPI_SSL_VERIFY'] = 'False'

        self.cb_client = CbResponseAPI()

        self.timeout_isolation_sec = 5

        self.parent_processes = []

    def sensors_count_by_group(self):
        api_result = {
            'agent': {
                'total': 0,
                'Online': 0,
                'Offline': 0
            }
        }
        sensors = ()

        for g in self.cb_client.select(SensorGroup):
            # specific group
            if g.name in Config.CB['TENANT']:
                api_result['agent']['total'] += int(g.number_of_hosts)
                for s in g.sensors:
                    if s.status not in api_result['agent']:
                        api_result['agent'][s.status] = 1
                    else:
                        api_result['agent'][s.status] += 1
        # return {'doc': api_result}
        return api_result

    def get_sensors_info_bygroup(self):
        api_result = []
        sensors = ()

        for g in self.cb_client.select(SensorGroup):
            # specific group
            if g.name in Config.CB['TENANT']:
                group_id = str(g.id)
                sensors = self.cb_client.select(Sensor).where("groupid:"+group_id)
        for sensor in sensors:
            endpoint = Endpoint(str(sensor.computer_name),str(sensor.dns_name),str(sensor.last_checkin_time),\
                                str(sensor.network_interfaces), str(sensor.os), str(sensor.status))
            api_result.append(endpoint.__dict__)
        print (json.dumps(api_result))

    def get_alert_bygroup(self):
        api_result = []
        
        #10080m = 7 days
        alerts = self.cb_client.select(Alert).where("created_time:-10080m")
        for alert in alerts:
            try:
                if(str(alert.sensor.group.name) == Config.CB['TENANT']):
                    try:
                        api_result.append(str(alert.original_document['description']))
                    except KeyError:
                        api_result.append(str(alert.original_document['watchlist_name']))
            except:
                pass
        print (json.dumps(api_result))

    def get_sensors_bygroup(self):
        for g in self.cb_client.select(SensorGroup):
            # specific group
            if g.name in Config.CB['TENANT']:
                group_id = str(g.id)
                sensors = self.cb_client.select(Sensor).where("groupid:"+group_id)
        return sensors
        
    def uninstallExceededSensor(self, sensors):
        for i,sensor in enumerate(sensors):
            # if (i > 99):
            if (sensor.id == 447):
                if (sensor.uninstall == False):
                    self.markUninstall(sensor.id)
        pass

    def markUninstall(self, sensorId):
        url =  Config.CB['BASE_URL'] + "/api/v1/sensor/" + str(sensorId)
        headers = {
        'X-Auth-Token': Config.CB['TOKEN'],
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=False)
        sensor_json = json.loads(response.text)
        
        payload = {
        "uninstall": 'true',
        "group_id": sensor_json['group_id']
        }
        headers = {
        'X-Auth-Token': Config.CB['TOKEN'],
        'Content-Type': 'application/json'
        }
        response = requests.request("PUT", url, headers=headers, data = json.dumps(payload), verify=False)
        print (response)
        
    def count_wl(self):
        api_result = []
        i=0
        wls = self.cb_client.select(Watchlist)
        for wl in wls:
            i = i +1
        
        print(i)
        # for alert in alerts:
        #     try:
        #         if(str(alert.sensor.group.name) == Config.CB['TENANT']):
        #             try:
        #                 api_result.append(str(alert.original_document['description']))
        #             except KeyError:
        #                 api_result.append(str(alert.original_document['watchlist_name']))
        #     except:
        #         pass
        # print (json.dumps(api_result))
    
    def get_feeds(self):
        feed_result = []
        feeds = self.cb_client.select(Feed)
        for feed in feeds:
            feedId = feed.id
            feedName = feed.name
            threatReports = self.get_report_from_feed(feedId)
            with open(feedName + '.json', 'w') as outfile:
                json.dump(threatReports, outfile)

    def get_report_from_feed(self, feedId):
        report_result = []
        threatReports = ((self.cb_client.select(Feed).where("id:"+ str(feedId))).first()).reports
        for report in threatReports:
            js = report.__dict__['_info']
            report_result.append(js)
        # with open('data.json', 'w') as outfile:
        #     json.dump(report_result, outfile)        
        return report_result
if __name__ == '__main__':
    client = CarbonBlackClient()
    # client.sensors_count_by_group()
    # client.get_sensors_bygroup()
    # client.get_alert_bygroup()
    # client.count_wl()
    client.get_feeds()
    # client.get_report_from_feed(14)

