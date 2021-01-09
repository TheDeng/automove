import random


class User:
    # 设置最大的负载值
    max_cpu = 30
    max_io = 30
    max_bandwidth = 30
    max_memory = 30
    # 设置用户userId
    userId = 0

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.id = User.userId
        User.userId = User.userId + 1
        self.request = self.get_random_request()
        self.within_servers = []
        self.op_server = []
        self.selected_server = []
        self.time=0

    # 初始化用户的工作负载
    def get_random_request(self):
        cpu = random.randint(0, User.max_cpu)
        # io = random.randint(0, User.max_io)
        bandwidth = random.randint(0, User.max_bandwidth)
        memory = random.randint(0, User.max_memory)
        return [cpu, bandwidth, memory]

    # 给用户所在的服务器列表添加服务器元素
    def append_server(self, server_id):
        self.within_servers.append(server_id)

    # 用户数据字典
    def info(self):
        return {'id': self.id, 'latitude': self.latitude, 'longitude': self.longitude, 'workload': self.workload,
                'within_servers': self.within_servers}

    def key_info(self):
        return {'id': self.id, 'workload': self.workload, 'within_servers': self.within_servers}

    def position(self):
        return {'coordinate': [self.latitude, self.longitude]}

    def random_move(self):
        self.way_one()

    def way_one(self):
        v_d = [1, -1, 0]
        unit = 0.0001
        self.latitude = self.latitude + random.choice(v_d) * unit
        self.longitude = self.longitude + random.choice(v_d) * unit

    # 返回资源请求向量
    def get_request(self):
        return self.request

    def set_request(self):
        self.request=self.get_random_request()
    # 设置可选服务器
    def set_op_server(self, op_server):

        self.op_server=op_server

    # 返回可选服务器
    def get_op_server(self):
        return self.op_server

    # 返回实选服务器
    def get_selected_server(self):
        return self.selected_server

    # 设置实选服务器
    def set_selected_server(self, selected_server):
        self.selected_server = selected_server

    # 返回当前用户的状态
    def get_user_status(self):
        return {
            "id": self.get_user_id(),
            "position": [round(self.latitude, 5), round(self.longitude, 5)],
            "request": self.get_request(),
            "op_server": self.get_op_server(),
            "selected_server": self.get_selected_server()
        }
    def get_user_id(self):
        return self.id

if __name__ == '__main__':
    user = User(122, 233)
    print(user.id)
