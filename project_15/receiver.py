import sys
import time
import random
from socket import *
from func6 import *

n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
G=(0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0)
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

if __name__ == '__main__':
    s=socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1',8080))
    print("与sender连接成功")
    d2=random.randint(1, n-1)
    print("子私钥d2：{}".format(d2))
    P1=s.recv(1024).decode('utf-8')
    print("收到P1")
    print("P1：{}".format(P1))
    _G=(G[0],p-G[1]) #-G
    P=add(mul(inverse_mod(d2,n),eval(P1)),_G)
    print("向sender发送公钥P")
    print("P：{}".format(P))
    s.send(str(P).encode('utf-8'))
    print("发送完毕")
    Q1=s.recv(1024).decode('utf-8')
    e=s.recv(1024).decode('utf-8')
    print("收到Q1和e")
    print("Q1：{}".format(Q1))
    print("e：{}".format(e))
    k2=random.randint(1, n-1)
    Q2=mul(k2,G)
    k3=random.randint(1, n-1)
    (x1,x2)=add(mul(k3,eval(Q1)),Q2)

    r=(x1+int(e,16))%n
    if r==0:
        print("出错")
        sys.exit() # 退出程序
    s2=(d2*k3)%n
    s3=(d2*(r+k2))%n
    
    print("向sender发送公钥r、s2和s3")
    print("r：{}".format(r))
    print("s2：{}".format(s2))
    print("s3：{}".format(s3))
    s.send(str(r).encode('utf-8'))
    time.sleep(1)
    s.send(str(s2).encode('utf-8'))
    time.sleep(1)
    s.send(str(s3).encode('utf-8'))
    print("发送完毕")
    result=s.recv(1024).decode('utf-8')
    print(result)
    s.close()
    print("与sender断开连接")
