from func4 import *
import secrets
import time
import socketserver

public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

class MyUdphandler(socketserver.BaseRequestHandler):  # 自定义类
    def handle(self):
        print("与receiver连接成功")
        print("向receiver发送enc_M和enc_K")
        print("enc_M：{}".format(enc_M))
        print("enc_K：{}".format(enc_K))
        self.request.send(enc_M)
        time.sleep(1)
        self.request.send(enc_K)
        print("发送完毕")
        enc_new_M= self.request.recv(1024)
        print("收到enc_new_M")
        print("enc_new_M：{}".format(enc_new_M))
        new_M=sm4_dec(enc_new_M,K)
        print("解得new_M")
        print("new_M：{}".format(new_M))
        self.request.close()
        self.server.shutdown()
        print("与receiver断开连接")


if __name__ == '__main__':
    M=b'Hello Friend.'
    K=secrets.randbits(128) #128bit
    K=bytes.fromhex(hex(K)[2:].zfill(32))
    print("M：{}".format(M))
    print("K：{}".format(K))
    enc_M=sm4_enc(M,K)
    enc_K=sm2_enc(K,public_key)
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8080),MyUdphandler)
    server.serve_forever()

