from socket import *
from func3 import *
import socketserver
import time

class MyUdphandler(socketserver.BaseRequestHandler):  # 自定义类
    def handle(self):
        print("与Bob连接成功")
        age_big = input('证明年龄大于：')
        print("向Bob发送证明年龄大于：{}".format(age_big))
        self.request.send(str(age_big).encode('utf-8'))
        print("发送完毕")
        p = Alice(s, int(age_big))
        print("向Bob发送p和sig_c")
        print("p：{}".format(p))
        print("sig_c：{}".format(sig_c))
        self.request.send(str(p).encode('utf-8'))
        time.sleep(1)
        self.request.send(str(sig_c).encode('utf-8'))
        print("发送完毕")
        result = self.request.recv(1024).decode('utf-8')
        print(result)
        self.request.close()
        self.server.shutdown()
        print("与Bob断开连接")
        
def Alice(s, age_big):
    d0 = (2021 - age_big) - int(born)
    for i in range(d0):
        s = SM3(s)
    p = s
    return p
        
if __name__ == '__main__':
    ss = socket(AF_INET, SOCK_STREAM)
    ss.connect(('127.0.0.1',8081))
    print("与Issuer连接成功")
    born = input('出生年份：')
    print("向Issuer发送出生年份：{}".format(born))
    ss.send(born.encode('utf-8'))
    print("发送完毕")
    s = ss.recv(1024).decode('utf-8')
    sig_c = ss.recv(1024).decode('utf-8')
    print("收到s和sig_c")
    print("s：{}".format(s))
    print("sig_c：{}".format(sig_c))
    ss.close()
    print("与Issuer断开连接")
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8080),MyUdphandler)
    server.serve_forever()
