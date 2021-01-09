from .User import User
from .Server import Server
from math import radians, cos, sin, asin, sqrt
import random

# 地球半径
EARTH_REDIUS = 6378.137


def get_all_user():
    user_list = []
    file = open("media/users-melbcbd-generated.csv", 'r+')
    for index, line in enumerate(file):
        if index == 0:
            continue
        latitude, longitude = line.split(',')
        user_list.append(User(float(latitude), float(longitude)))

    return user_list


def get_all_server():
    server_list = []
    file = open("media/site-optus-melbCBD.csv", 'r+')
    for index, line in enumerate(file):
        if index == 0:
            continue
        result = line.split(',')
        server_list.append(Server(float(result[1]), float(result[2])))

    return server_list


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


# 获取用户在哪些服务器的覆盖范围的信息
def get_within_servers(user_list, server_list):
    for user in user_list:
        for server in server_list:
            result = judge_cov(user, server)
            if result:
                user.append_server(server.id)


# 获取服务器的总的剩余capactiy,比例为rate,可以取值为1,1.5,3
def get_remain_capacity(user_list, rate):
    capacity = [0, 0, 0, 0]
    for user in user_list:
        workload = user.workload
        capacity[0] = capacity[0] + workload[0]
        capacity[1] = capacity[1] + workload[1]
        capacity[2] = capacity[2] + workload[2]
        capacity[3] = capacity[3] + workload[3]
    capacity[0] = capacity[0] * rate
    capacity[1] = capacity[1] * rate
    capacity[2] = capacity[2] * rate
    capacity[3] = capacity[3] * rate
    return capacity


# 为每个服务器分配capacity
def allocate_capacity(server_list, capacity):
    s_size = len(server_list)
    cpu_max = int(capacity[0] * 2 / s_size)
    cpu_min = int(capacity[0] / 10 / s_size)
    io_max = int(capacity[1] * 2 / s_size)
    io_min = int(capacity[1] / 10 / s_size)
    bandwidth_max = int(capacity[2] * 2 / s_size)
    bandwidth_min = int(capacity[2] / 10 / s_size)
    memory_max = int(capacity[3] * 2 / s_size)
    memory_min = int(capacity[3] / 10 / s_size)
    for server in server_list:
        server.capacity = [random.randint(cpu_min, cpu_max), random.randint(io_min, io_max),
                           random.randint(bandwidth_min, bandwidth_max), random.randint(memory_min, memory_max)]


def init_data():
    user_list = get_all_user()
    server_list = get_all_server()
    get_within_servers(user_list, server_list)
    capacity = get_remain_capacity(user_list, 1)
    print(capacity)
    allocate_capacity(server_list, capacity)
    for s in server_list:
        print(s.key_info())
    return user_list, server_list
