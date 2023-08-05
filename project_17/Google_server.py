import time
import random
import socketserver
from func3 import *

class MyUdphandler(socketserver.BaseRequestHandler):  # 自定义类
    def handle(self):
        print("与client连接成功")
        data_records={"abc":"123","hhhhtttgxy":"52831a0D","abcdefg_":"0123456","user777":"89890146a","yyyyytsey":"17yh00_3","331305yo8b":"88887777"}
        p=3587784517 # 素数
        b=random.randint(1, p-1)
        sk=b
        key_value_table={}

        for i in range(65536): # 初始化
            key_value_table[hex(i)[2:].zfill(4)]=set()
            
        for item in data_records.items():
            hi=H(item[0]+item[1]) # 用sm3代替Argon2
            ki=hi[:4] # 2bytes对应4个16进制数
            vi=pow(int(hi,16),b,p)
            key_value_table[ki].add(vi)

        k_v=self.request.recv(1024).decode('utf-8')
        print("收到(k,v)")
        print("(k,v)：{}".format(k_v))
        k,v=eval(k_v)
        hab=pow(v,b,p)
        S=key_value_table[k]
        
        print("向client发送hab和S")
        print("hab：{}".format(hab))
        print("S：{}".format(S))
        self.request.send(str(hab).encode('utf-8'))
        time.sleep(1)
        self.request.send(str(S).encode('utf-8'))
        print("发送完毕")
        
        self.request.close()
        self.server.shutdown()
        print("与client断开连接")
        
if __name__ == '__main__':
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8080),MyUdphandler)
    server.serve_forever()


