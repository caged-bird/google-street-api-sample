#coding=utf-8
import time
import shutil
import requests

#BOTTOM_LEFT = [41.824709, 140.778092]
BOTTOM_LEFT = [41.827479000000004,140.78998199999964]


API_KEY='AIzaSyAuFSNbwPRNUGngezs9AZVGEqAf8iV00kU'

LAT_UNIT = 0.000554
LONG_UNIT = 0.00041

UP_RIGHT = [41.839469, 140.803125]
#BOTTOM_LEFT = [41.802199, 140.774635] # 白百合

SIZE = '640x600'
headings = [0.0, 90.0, 180.0, 270.0]

lati = BOTTOM_LEFT[0]
longi = BOTTOM_LEFT[1]
while lati < UP_RIGHT[0]:
    time.sleep(1)
    longi = BOTTOM_LEFT[1]
    while longi < UP_RIGHT[1]:
        for heading in headings:
            loc = [lati, longi]
            url = "https://maps.googleapis.com/maps/api/streetview?size="+str(SIZE)+"&location="+','.join([str(loc[0]), str(loc[1])])+"&heading="+str(heading)+"&pitch=0.0&fov=180.0&zoom=1&key=" + API_KEY
            response = requests.get(url, stream=True)
            file_name = 'images/' + ','.join([str(loc[0]), str(loc[1])]) + "," + str(heading) + '.jpg'
            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(file_name)
            time.sleep(0.5)
        longi += LONG_UNIT
    lati += LAT_UNIT
