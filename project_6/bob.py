from socket import *
from func3 import *

public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

def Bob(p, sig_c, age_big):
    d1 = 2100 - (2021 - age_big)
    for i in range(d1):
        p = SM3(p)
    c_ = p
    return SM2_verify(sig_c, bytes.fromhex(c_),public_key)

if __name__ == '__main__':
    ss = socket(AF_INET, SOCK_STREAM)
    ss.connect(('127.0.0.1',8080))
    print("与Alice连接成功")
    age_big = ss.recv(1024).decode('utf-8')
    print("收到Alice想证明她的年龄大于{}".format(age_big))
    p = ss.recv(1024).decode('utf-8')
    sig_c = ss.recv(1024).decode('utf-8')
    print("收到p和sig_c")
    print("p：{}".format(p))
    print("sig_c：{}".format(sig_c))
    
    if Bob(p, sig_c, int(age_big)):
        print("验证成功")
        print("告知Alice验证通过")
        ss.send('验证通过'.encode('utf-8'))
    else:
        print("验证失败")
        print("告知Alice验证未通过")
        ss.send('验证未通过'.encode('utf-8'))
    
    ss.close()
    print("与Alice断开连接")
    
