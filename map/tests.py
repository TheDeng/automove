
from math import radians, cos, sin, asin, sqrt
import random
import os

# 地球半径
EARTH_REDIUS = 6378.137
ROOT_PATH='../media/experiment_data/'
PRE="ex_"
POST=".json"

# 判断一个用户是否在一个服务器的覆盖范围内，如果是则返回true,否则返回false
def judge_cov(user, server):
    lat1 = user.latitude
    lng1 = user.longitude
    lat2 = server.latitude
    lng2 = server.longitude
    distance = geo_distance(lng1, lat1, lng2, lat2)
    cov = server.coverage
    if distance <= cov:
        return True
    else:
        return False


# 计算两经纬度点之间距离
def geo_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371 * 1000
    return dis

def create_json():
    for i in range(100):
        newfile=ROOT_PATH+PRE+str(i)+POST
        if not os.path.exists(newfile):
            f=open(newfile,"w")
            f.close()
            print(newfile+"created")
            return newfile

