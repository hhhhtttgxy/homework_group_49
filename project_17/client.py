import random
from socket import *
from func3 import *

if __name__ == '__main__':
    username=input("用户名：")
    password=input("密码：")
    
    s=socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1',8080))
    print("与server连接成功")
    p=3587784517 #素数
    while True:
        a=random.randint(1, p-1)
        if gcd(a,p-1)==1:
            break
    skc=a
    h=H(username+password) # 用sm3代替Argon2
    k=h[:4] # 2bytes对应4个16进制数
    v=pow(int(h,16),a,p)
    print("向server发送(k,v)")
    print("(k,v)：{}".format((k,v)))
    s.send(str((k,v)).encode('utf-8'))
    print("发送完毕")
    hab=s.recv(1024).decode('utf-8')
    S=s.recv(1024).decode('utf-8')
    print("收到hab和S")
    print("hab：{}".format(hab))
    print("S：{}".format(S))
    inverse_a=inverse_mod(a,p-1)
    hb=pow(int(hab),inverse_a,p)
    if hb in eval(S):
        print("已泄露")
    else:
        print("未泄露")
    s.close()
    print("与server断开连接")
