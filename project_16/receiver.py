from socket import *
from func9 import *

n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
G=(0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0)
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

if __name__ == '__main__':
    s=socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1',8080))
    print("与sender连接成功")
    d2=45107332754902873454879211549814471033736075779386003923213116589908529276156
    print("子私钥d2：{}".format(d2))
    T1=s.recv(1024).decode('utf-8')
    print("收到T1")
    print("T1：{}".format(T1))
    T2=mul(inverse_mod(d2,n),eval(T1))
    print("向sender发送T2")
    print("T2：{}".format(T2))
    s.send(str(T2).encode('utf-8'))
    print("发送完毕")
    result=s.recv(1024).decode('utf-8')
    print(result)
    s.close()
    print("与sender断开连接")
