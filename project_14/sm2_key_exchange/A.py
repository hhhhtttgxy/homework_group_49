import sys
import random
import socketserver
from func7 import *
from math import log2,ceil

p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
G=(0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D,0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2)
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7

IDA="414C494345313233405941484F4F2E434F4D"
IDB="42494C4C343536405941484F4F2E434F4D"
ENTLA=hex(len(IDA)*4)[2:].zfill(4)
ENTLB=hex(len(IDB)*4)[2:].zfill(4)
klen=128

dA=0x6FCBA2EF9AE0AB902BC3BDE3FF915D44BA4CC78F88E2F8E7F8996D3B8CCEEDEE
PA=(0x3099093BF3C137D8FCBBCDF4A2AE50F3B0F216C3122D79425FE03A45DBFE1655,0x3DF79E8DAC1CF0ECBAA2F2B49D51A4B387F2EFAF482339086A27A8E05BAED98B)

PB=(0x245493D446C38D8CC0F118374690E7DF633A8A4BFB3329B5ECE604B2B4F37F43,0x53C0869F4B9E17773DE68FEC45E14904E0DEA45BF6CECF9918C85EA047C60A4C)

class MyUdphandler(socketserver.BaseRequestHandler):  # 自定义类
    def handle(self):
        print("与B连接成功")
        ZA=H(ENTLA+IDA+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(PA[0])[2:].zfill(64)+hex(PA[1])[2:].zfill(64))
        ZB=H(ENTLB+IDB+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(PB[0])[2:].zfill(64)+hex(PB[1])[2:].zfill(64))
          
        w=ceil(ceil(log2(n))/2)-1
        #rA=random.randint(1,n-1)
        rA=0x83A2C9C8B96E5AF70BD480B472409A9A327257F1EBB73F5B073354B248668563

        RA=mul(rA,G)
        print("向B发送RA")
        print("RA：{}".format(RA))
        self.request.send(str(RA).encode('utf-8'))
        print("发送完毕")
        (x1,y1)=RA
        print("x1：{}".format(hex(x1)[2:]))
        print("y1：{}".format(hex(y1)[2:]))

        x1_=pow(2,w)+(x1&(pow(2,w)-1))
        print("x1_：{}".format(hex(x1_)[2:]))
        tA=(dA+x1_*rA)%n
        print("tA：{}".format(hex(tA)[2:]))
        RB=self.request.recv(1024).decode('utf-8')
        SB=self.request.recv(1024).decode('utf-8')
        print("收到RB和SB")
        print("RB：{}".format(RB))
        print("SB：{}".format(SB))
        
        (x2,y2)=eval(RB)
        if (pow(y2,2))%p!=(pow(x2,3)+a*x2+b)%p:
            print("出错")
            sys.exit()
            
        x2_=pow(2,w)+(x2&(pow(2,w)-1))
        print("x2_：{}".format(hex(x2_)[2:]))
        

        U=mul(tA,add(PB,mul(x2_,eval(RB))))
        if U==(0,0):
            print("出错")
            sys.exit()
            
        (xU,yU)=U
        print("xU：{}".format(hex(xU)[2:]))
        print("yU：{}".format(hex(yU)[2:]))
        KA=KDF(hex(xU)[2:].zfill(64)+hex(yU)[2:].zfill(64)+ZA+ZB,klen)
        print("共享密钥KA：{}".format(KA))
        S1=H("02"+hex(yU)[2:].zfill(64)+H(hex(xU)[2:].zfill(64)+ZA+ZB+hex(x1)[2:].zfill(64)+hex(y1)[2:].zfill(64)+hex(x2)[2:].zfill(64)+hex(y2)[2:].zfill(64)))
        print("S1：{}".format(S1))
        if S1!=SB:
            print("出错")
            sys.exit()
            
        SA=H("03"+hex(yU)[2:].zfill(64)+H(hex(xU)[2:].zfill(64)+ZA+ZB+hex(x1)[2:].zfill(64)+hex(y1)[2:].zfill(64)+hex(x2)[2:].zfill(64)+hex(y2)[2:].zfill(64)))
        print("向B发送SA")
        print("SA：{}".format(SA))
        self.request.send(SA.encode('utf-8'))
        print("发送完毕")
        self.request.close()
        self.server.shutdown()
        print("与B断开连接")
        
if __name__ == '__main__':
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8080),MyUdphandler)
    server.serve_forever()
