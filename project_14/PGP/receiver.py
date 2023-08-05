from socket import *
from func4 import *

private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1',8080))
    print("与sender连接成功")
    enc_M = s.recv(1024)
    enc_K = s.recv(1024)
    print("收到enc_M和enc_K")
    print("enc_M：{}".format(enc_M))
    print("enc_K：{}".format(enc_K))
    K=sm2_dec(enc_K,private_key)
    M=sm4_dec(enc_M,K)
    print("解得K和M")
    print("K：{}".format(K))
    print("M：{}".format(M))
    new_M=b'Hello Friend, I have received.'
    print("new_M：{}".format(new_M))
    enc_new_M=sm4_enc(new_M,K)
    print("向sender发送一个加密后的新消息")
    print("enc_new_M：{}".format(enc_new_M))
    s.send(enc_new_M)
    print("发送完毕")
    s.close()
    print("与sender断开连接")

