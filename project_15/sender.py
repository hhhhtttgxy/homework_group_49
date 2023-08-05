import sys
import time
import random
import hashlib
import socketserver
from func6 import *

n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
G=(0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0)
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

class MyUdphandler(socketserver.BaseRequestHandler):  # 自定义类
    def handle(self):
        print("与receiver连接成功")
        d1=random.randint(1, n-1)
        print("子私钥d1：{}".format(d1))
        P1=mul(inverse_mod(d1, n),G)
        print("向receiver发送P1")
        print("P1：{}".format(P1))
        self.request.send(str(P1).encode('utf-8'))
        print("发送完毕")
        P=self.request.recv(1024).decode('utf-8')
        print("收到公钥P")
        print("P：{}".format(P))
        M='Hello Friend'
        Z='Alice_Bob'
        M_=Z+M
        e=sha_256(M_)
        k1=random.randint(1,n-1)
        Q1=mul(k1, G)
        print("向receiver发送Q1和e")
        print("Q1：{}".format(Q1))
        print("e：{}".format(e))
        self.request.send(str(Q1).encode('utf-8'))
        time.sleep(1)
        self.request.send(e.encode('utf-8'))
        print("发送完毕")

        r=self.request.recv(1024).decode('utf-8')
        s2=self.request.recv(1024).decode('utf-8')
        s3=self.request.recv(1024).decode('utf-8')
        print("收到r、s2和s3")
        print("r：{}".format(r))
        print("s2：{}".format(s2))
        print("s3：{}".format(s3))

        s=((d1*k1)*int(s2)+d1*int(s3)-int(r))%n
        if s==0 and s==n-r:
            print("运算出错")
            sys.exit() # 退出程序
        else:
            sign=(int(r),s)
            print("签名成功")
            print("告知receiver签名成功")
            self.request.send("签名成功".encode('utf-8'))
            print("(r,s)：{}".format(sign))

        self.request.close()
        self.server.shutdown()
        print("与receiver断开连接")

if __name__ == '__main__':
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8080),MyUdphandler)
    server.serve_forever()
