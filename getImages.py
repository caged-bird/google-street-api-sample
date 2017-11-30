#coding=utf-8
import time
import shutil
import requests
import json
from const import get_slack_key
from const import get_google_key

LAT_UNIT = 0.000554
LONG_UNIT = 0.00041

#BOTTOM_LEFT = [41.802199, 140.774635] # 白百合
#BOTTOM_LEFT = [41.824709, 140.778092]
BOTTOM_LEFT = [41.827479000000004, 140.78998199999964]
UP_RIGHT = [41.839469, 140.803125]

SIZE = '640x600'
headings = [0.0, 90.0, 180.0, 270.0]

lati = BOTTOM_LEFT[0]
longi = BOTTOM_LEFT[1]
while lati < UP_RIGHT[0]:
    longi = BOTTOM_LEFT[1]
    while longi < UP_RIGHT[1]:
        for heading in headings:
            loc = [lati, longi]
            meta_url = 'https://maps.googleapis.com/maps/api/streetview/metadata?size='+str(SIZE)+"&location="+','.join([str(loc[0]), str(loc[1])])+"&heading="+str(heading)+"&pitch=0.0&fov=180.0&zoom=1&key=" + get_google_key()
            response = requests.get(meta_url, stream=True)
            if response.json()["status"] in "OK":
                url = "https://maps.googleapis.com/maps/api/streetview?size="+str(SIZE)+"&location="+','.join([str(loc[0]), str(loc[1])])+"&heading="+str(heading)+"&pitch=0.0&fov=180.0&zoom=1&key=" + get_google_key()
                response = requests.get(url, stream=True)
                file_name = '../images/' + ','.join([str(loc[0]), str(loc[1])]) + "," + str(heading) + '.jpg'
                with open(file_name, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                print(file_name)
            elif response.json()["status"] in "OVER_QUERY_LIMIT":
                print("over_query_limit")
                url = "https://hooks.slack.com/services/" + get_slack_key()
                requests.post(url, data=json.dumps({
                    'username': "endnotifier",
                    'link_names': 1,
                    'attachments': [{
                        "text": u"上限超えました",
                    }]
                }))
                break
            time.sleep(0.5)
        longi += LONG_UNIT
    lati += LAT_UNIT

url = "https://hooks.slack.com/services/" + get_slack_key()
requests.post(url, data=json.dumps({
    'username': "endnotifier",
    'link_names': 1,
    'attachments': [{
        "text": u"終わりましたよ",
    }]
}))
