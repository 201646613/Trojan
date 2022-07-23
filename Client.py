#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/7/23 10:05 
# @Author : 201646613 
# @Version：V 1.0
# @File : Client.py
# @desc :


from socket import socket
from json import dumps
from time import time


class Client:  # 定义客户端类，实现命名传输，和结果回显
    __Ser_PORT: int

    def __init__(self, HOST: str, PORT: int):  # 初始化连接
        self.__Ser_HOST = HOST
        self.__Ser_PORT = PORT
        self.__Client_name = int(time())
        addr = (HOST, PORT)
        self.__listen = socket()
        self.__listen.connect(addr)
        self.__listen.sendall(str(self.__Client_name).encode(encoding='utf-8'))  # 发送时间戳身份认证
        print(self.__listen.recv(1024).decode('utf-8'))   # 接受信息
        print("Target info: {}".format(self.__listen.recv(1024).decode('utf-8')))  # 接受信息

        self.main()

    def main(self):  # 主函数

        while True:
            self.user_input()

    def cmd_exec(self, data: str) -> bytes:  # cmd 执行函数

        a = {'type': 'cmd', 'data': data}
        j = dumps(a).encode('utf-8')
        self.__listen.sendall(j)

        recv = self.__listen.recv(1024000)
        return recv

    def get_fun_date(self, s: str) -> list:
        a = []
        s = s.split(' ')
        a.append(s[0])
        del s[0]
        a.append(" ".join(s))
        return a

    def user_input(self):
        fun_list = ['cmd', 'shell']  # 可执行函数列表
        a = input("Console:>> ")  # 接受用户输入
        a = self.get_fun_date(a)  # 提取关键词
        if a[0] not in fun_list:  # 判断用户输入指令是否可执行
            print("{}：暂不支持该函数".format(a[0]))
        if a[0] == 'cmd' or a[0] == 'shell':
            recv = self.cmd_exec(a[1])
            try:
                print(str(recv.decode('gbk')))
            except Exception as e:
                print(recv.decode())
                # print(str(recv).encode("utf-8"))



T = Client("127.0.0.1", 16220)
