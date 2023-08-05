import sys
import socketserver
from socket import *
from func9 import *

n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
G=(0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0)
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

class MyUdphandler(socketserver.BaseRequestHandler):  # 自定义类
    def handle(self):
        print("与receiver连接成功")
        d1=11284301686100593435272859766142206662001417249657340699489350582178954335384
        print("子私钥d1：{}".format(d1))
        C1,C2,C3=eval(C)
        C1=(int(C1[0],16),int(C1[1],16))
        if C1[0]==0 and C1[0]==0:
            print("出错")
            sys.exit() # 退出程序
        T1=mul(inverse_mod(d1, n),C1)
        print("向receiver发送T1")
        print("T1：{}".format(T1))
        self.request.send(str(T1).encode('utf-8'))
        print("发送完毕")
        T2=self.request.recv(1024).decode('utf-8')
        print("收到T2")
        print("T2：{}".format(T2))
        _C1=(C1[0],p-C1[1]) #-C1
        (x2,y2)=add(eval(T2),_C1)
        klen=len(C2)*4
        t=KDF(hex(x2)[2:].zfill(64)+hex(y2)[2:].zfill(64),klen)
        M__=int(C2,16)^int(t,16)
        u=H(hex(x2)[2:].zfill(64)+hex(M__)[2:].zfill(klen//4)+hex(y2)[2:].zfill(64))
        if u==C3:
            print("解密成功")
            print("告知receiver解密成功")
            self.request.send("解密成功".encode('utf-8'))
            print(bytes.fromhex(hex(M__)[2:].zfill(klen//4)))
            
        self.request.close()
        self.server.shutdown()
        print("与receiver断开连接")

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1',8081))
    print("与加密者连接成功")
    C = s.recv(1024).decode('utf-8')
    print("收到密文C")
    print("C：{}".format(C))
    s.close()
    print("与加密者断开连接")
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8080),MyUdphandler)
    server.serve_forever()
