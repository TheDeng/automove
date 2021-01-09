from django.shortcuts import render
from .Utils import get_all_server,get_all_user
from django.http import HttpResponse
import random
import json
from django.views.decorators.csrf import csrf_exempt
from math import radians, cos, sin, asin, sqrt
import os

import numpy as np

# 地球半径
EARTH_REDIUS = 6378.137


sample_user=[]
sample_server=[]
record={}
whole_time=0


def generate_data(request):
    global record
    if record=={"whole_time":0,"user":{},"server":{}}:
        retundata = json.dumps({"res": "succeed"})
        return HttpResponse(retundata, content_type="application/json")
    record_file ="ex_data.json"
    f=open(record_file,"w")
    jsondata=json.dumps(record)
    f.writelines(jsondata+"\n")
    f.flush()
    retundata = json.dumps({"res":"succeed"})
    return HttpResponse(retundata, content_type="application/json")

# def create_json():
#
#
#     for i in range(0,100):
#         newfile="ex_"+str(i)+".json"
#         if not os.path.exists(newfile):
#             f=open(newfile,"a")
#             f.close()
#             print(newfile+" created")
#             return newfile



def init():
    global sample_server,sample_user,record
    record={"whole_time":whole_time,  "user": {}, "server": {}}
    all_user=get_all_user()
    all_server=get_all_server()
    sample_user=random.sample(all_user,50)
    for index ,u in enumerate(sample_user):
        u.id=index+1
        record["user"][u.get_user_id()]=[]


    sample_server=random.sample(all_server,50)
    for index,s in enumerate(sample_server):
        s.id=index+1
        record["server"][s.get_server_id()]=[]


    return sample_user,sample_server

# Create your views here.
def index(request):

    return render(request,"../templates/map.html")

def env(request):
    return render(request, "../templates/newmap.html")

def load(request):
    global sample_user,sample_server
    sample_user, sample_server = init()
    user_list=[]
    server_list=[]
    for u in sample_user:
        user_list.append(u.position())
    for s in sample_server:
        server_list.append(s.position())
    jsondata=json.dumps({"userlist":user_list,"serverlist":server_list})
    return HttpResponse(jsondata,content_type="application/json")

def move(request):
    global sample_user, sample_server
    #首先清除上次的缓存
    clear(sample_user,sample_server)
    #首先进行位置的更新

    for u in sample_user:
        u.random_move()
    user_list=[]
    for u in sample_user:
        user_list.append(u.position())
    #位置更新完之后执行请求的更新
    update_request(sample_user,sample_server)
    jsondata=json.dumps(user_list)
    return HttpResponse(jsondata,content_type="application/json")

def clear(sample_user,sample_server):
    for u in sample_user:
        u.set_request()
        u.set_op_server([])
        u.set_selected_server([])
    for s in sample_server:
        s.refresh_capacity()
        s.set_held_user([])


@csrf_exempt
def get_user_status(request):
    global sample_user,record
    user_status={"total":len(sample_user),"rows":[]}

    for u in sample_user:
        user_status["rows"].append(u.get_user_status())
        record["user"][u.get_user_id()].append(u.get_user_status())

    jsondata=json.dumps(user_status)

    return HttpResponse(jsondata, content_type="application/json")



@csrf_exempt
def get_server_status(request):
    global sample_server,record
    server_status={"total":len(sample_server),"rows":[]}
    for s in sample_server:
        server_status["rows"].append(s.get_server_status())
        record["server"][s.get_server_id()].append(s.get_server_status())

    jsondata=json.dumps(server_status)

    return HttpResponse(jsondata, content_type="application/json")

def update_request(sample_user,sample_server):
    global record,whole_time
    whole_time=whole_time+1
    record["whole_time"]=whole_time
    for user in sample_user:
        #获取距离范围之内服务器
        covered_server=get_covered_server(user,sample_server)
        if len(covered_server)!=0:
            #获取资源范围之内服务器
            op_server=get_op_server(user,covered_server)
            if len(op_server)!=0:
                 #获取实选服务器
                 get_selected_server(user,op_server)

#获取用户位于范围之内的服务器列表
def get_covered_server(user,sample_server):
    covered_server_list=[]
    for server in sample_server:
        if judge_cov(user,server):
            covered_server_list.append(server)
    return covered_server_list
#获取有足够资源的服务器列表
def get_op_server(user,covered_server_list):
    if len(covered_server_list)==0:
        return
    op_server=[]
    for server in covered_server_list:
        if judge_serve(user,server):
            op_server.append(server)
    #设置用户的可选服务器属性
    op_list = []
    for s in op_server:
        op_list.append(s.get_server_id())
    user.set_op_server(op_list)
    return op_server

#从待选服务器中随机选一个作为实选服务器
def get_selected_server(user,op_server):
    if len(op_server)==0:
        return
    server=random.choice(op_server)
    #实选服务器减去资源请求
    server.decrease_capacity(user)
    #设置实选服务器服务的用户列表
    server.append_held_user(user.get_user_id())
    #设置用户的实选服务器属性
    user.set_selected_server([server.get_server_id()])


#判断一个服务器是否有足够资源服务一个用户
def judge_serve(user,server):
    is_ok = True
    temp=[0,0,0]
    s=server.get_capacity()
    u=user.get_request()
    temp[0]=s[0]-u[0]
    temp[1]=s[1]-u[1]
    temp[2]=s[2]-u[2]
    # 服务器资源减去用户的请求

    # 判断有无小于零的项目
    for c in temp:
        if c < 0:
            is_ok = False
            break
    return is_ok

# 判断一个用户是否在一个服务器的覆盖范围内，如果是则返回true,否则返回false
def judge_cov(user, server):
    lat1 = user.latitude
    lng1 = user.longitude
    lat2 = server.latitude
    lng2 = server.longitude
    distance = geo_distance(lng1, lat1, lng2, lat2)
    cov = server.get_coverage()
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


