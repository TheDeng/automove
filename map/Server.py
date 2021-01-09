import random
import numpy as np

class Server:
    # 设置最大的负载值
    max_cpu = 200
    max_bandwidth = 200
    max_memory = 200
    # 设置服务器server_id
    server_id = 0
    max_capacity=[200,200,200]
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.id = Server.server_id
        Server.server_id = Server.server_id + 1
        self.coverage = 100+random.randint(1,21)*10

        self.capacity = Server.max_capacity[:]

        # self.whole_capacity=[self.capacity[0],self.capacity[1],self.capacity[2]]

        self.status = random.choice(["on", "off"])
        self.held_user = []
        self.time=0

    # 随机初始化服务器的服务容量
    def get_random_capacity(self):
        cpu = random.randint(100, Server.max_cpu)
        bandwidth = random.randint(100, Server.max_bandwidth)
        memory = random.randint(100, Server.max_memory)
        return [cpu, bandwidth, memory]

    # 服务器数据字典
    def info(self):
        return {'id': self.id, 'latitude': self.latitude, 'longitude': self.longitude, 'coverage': self.coverage,
                'capacity': self.capacity}

    def key_info(self):
        return {'id': self.id, 'capacity': self.capacity}

    def position(self):
        return {'coordinate': [self.latitude, self.longitude], 'coverage': self.coverage}

    def get_server_status(self):
        return {
            "id": self.id,
            "position": [round(self.latitude, 5), round(self.longitude, 5)],
            "capacity": self.get_capacity(),
            "held_user": self.get_held_user(),
            "coverage": [self.get_coverage()]
        }

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_capacity(self):
        return self.capacity

    def set_held_user(self, held_user):
        self.held_user = held_user

    def get_held_user(self):
        return self.held_user

    def get_status(self):
        return self.status

    def append_held_user(self, user_id):
        self.held_user.append(user_id)

    def set_coverage(self,coverage):
        self.coverage=coverage
    def get_coverage(self):
        return self.coverage

    def decrease_capacity(self,user):
        capacity=self.get_capacity()
        request=user.get_request()
        if capacity[0]-request[0]>=0:
            capacity[0]=capacity[0]-request[0]
        if capacity[1] - request[1] >= 0:
            capacity[1]=capacity[1]-request[1]
        if capacity[2] - request[2] >= 0:
            capacity[2]=capacity[2]-request[2]
        self.set_capacity(capacity)

    def get_server_id(self):
        return self.id

    def refresh_capacity(self):
        self.capacity=Server.max_capacity[:]
