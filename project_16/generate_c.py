from func9 import *
import socketserver

P=(0xB9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A8308,0x1A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207)

class MyUdphandler(socketserver.BaseRequestHandler):  # 自定义类
    def handle(self):
        print("与sender连接成功")
        M=b"Hello Friend"
        C=sm2_enc(M.hex(), P)
        print("向sender发送密文")
        print("C：{}".format(C))
        self.request.send(str(C).encode('utf-8'))
        print("发送完毕")
        self.request.close()
        self.server.shutdown()
        print("与sender断开连接")
        
if __name__ == '__main__':
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8081),MyUdphandler)
    server.serve_forever()
