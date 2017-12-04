#coding=utf-8
import time
import shutil
import requests
import json
from constants.api_keys import KEY_SLACK
from constants.api_keys import KEY_STREET
from constants.geo_info import LAT_UNIT
from constants.geo_info import LONG_UNIT
from constants.geo_info import TARGET
from constants.geo_info import FOV
from constants.geo_info import PITCH

SIZE = '640x600'
headings = [0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0]

lati = TARGET.bottomleft[0]
longi = TARGET.bottomleft[1]
while lati < TARGET.upright[0]:
    longi = TARGET.bottomleft[1]
    while longi < TARGET.upright[1]:
        for heading in headings:
            loc = [lati, longi]
            meta_url = 'https://maps.googleapis.com/maps/api/streetview/metadata?size='+str(SIZE)+"&location="+','.join([str(loc[0]), str(loc[1])])+"&heading="+str(heading)+"&pitch=" + str(PITCH) + "&fov=" + str(FOV) + "&zoom=1&key=" + KEY_STREET
            response = requests.get(meta_url, stream=True)
            if response.json()["status"] in "OK":
                url = "https://maps.googleapis.com/maps/api/streetview?size="+str(SIZE)+"&location="+','.join([str(loc[0]), str(loc[1])])+"&heading="+str(heading)+"&pitch=" + str(PITCH) + "&fov=" + str(FOV) + "&zoom=1&key=" + KEY_STREET
                response = requests.get(url, stream=True)
                file_name = './images/' + ','.join([str(loc[0]), str(loc[1])]) + "," + str(heading) + '.jpg'
                with open(file_name, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                print(file_name)
            elif response.json()["status"] in "OVER_QUERY_LIMIT":
                print("over_query_limit")
                url = "https://hooks.slack.com/services/" + KEY_SLACK
                requests.post(url, data=json.dumps({
                    'username': "endnotifier",
                    'link_names': 1,
                    'attachments': [{
                        "text": u"上限超えました",
                    }]
                }))
                break
            else:
                print("no iamge")
            time.sleep(0.5)
        longi += LONG_UNIT
    lati += LAT_UNIT

url = "https://hooks.slack.com/services/" + KEY_SLACK
requests.post(url, data=json.dumps({
    'username': "endnotifier",
    'link_names': 1,
    'attachments': [{
        "text": u"画像収集終わりかい？",
    }]
}))
