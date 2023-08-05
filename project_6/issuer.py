import socketserver
import secrets
import time
from func3 import *

private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    
class MyUdphandler(socketserver.BaseRequestHandler):  # 自定义类
    def handle(self):
        print("与Alice连接成功")
        born = self.request.recv(1024).decode('utf-8')
        print('收到Alice的出生年份：{}'.format(born))
        s, sig_c = Issuer(int(born))
        print("向Alice发送s和sig_c")
        print("s：{}".format(s))
        print("sig_c：{}".format(sig_c))
        self.request.send(str(s).encode('utf-8'))
        time.sleep(1)
        self.request.send(str(sig_c).encode('utf-8'))
        print("发送完毕")
        self.request.close()
        self.server.shutdown()
        print("与Alice断开连接")
        
def Issuer(born):
    seed = secrets.randbits(128)
    s = SM3(hex(seed)[2:].zfill(32))
    c = s
    k = 2100 - born
    for i in range(k):
        c = SM3(c)
    sig_c = SM2_sign(bytes.fromhex(c),private_key)
    return s, sig_c
   
if __name__ == '__main__':
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8081),MyUdphandler)
    server.serve_forever()
