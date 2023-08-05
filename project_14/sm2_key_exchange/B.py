import sys
import time
import random
from func7 import *
from math import log2,ceil
from socket import *

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

dB=0x5E35D7D3F3C54DBAC72E61819E730B019A84208CA3A35E4C2E353DFCCB2A3B53

PB=(0x245493D446C38D8CC0F118374690E7DF633A8A4BFB3329B5ECE604B2B4F37F43,0x53C0869F4B9E17773DE68FEC45E14904E0DEA45BF6CECF9918C85EA047C60A4C)

PA=(0x3099093BF3C137D8FCBBCDF4A2AE50F3B0F216C3122D79425FE03A45DBFE1655
,0x3DF79E8DAC1CF0ECBAA2F2B49D51A4B387F2EFAF482339086A27A8E05BAED98B)

if __name__ == '__main__':
    s=socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1',8080))
    print("与A连接成功")
    ZA=H(ENTLA+IDA+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(PA[0])[2:].zfill(64)+hex(PA[1])[2:].zfill(64))
    ZB=H(ENTLB+IDB+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(PB[0])[2:].zfill(64)+hex(PB[1])[2:].zfill(64))
    w=ceil(ceil(log2(n))/2)-1
    #rB=random.randint(1,n-1)
    rB=0x33FE21940342161C55619C4A0C060293D543C80AF19748CE176D83477DE71C80

    
    RA=s.recv(1024).decode('utf-8')
    print("收到RA")
    print("RA：{}".format(RA)) 
    
    RB=mul(rB,G)

    (x2,y2)=RB
    print("x2：{}".format(hex(x2)[2:]))
    print("y2：{}".format(hex(y2)[2:]))
    
    x2_=pow(2,w)+(x2&(pow(2,w)-1))
    print("x2_：{}".format(hex(x2_)[2:]))
    tB=(dB+x2_*rB)%n
    print("tB：{}".format(hex(tB)[2:]))
    (x1,y1)=eval(RA)
    if (pow(y1,2))%p!=(pow(x1,3)+a*x1+b)%p:
        print("出错")
        sys.exit()
    x1_=pow(2,w)+(x1&(pow(2,w)-1))
    print("x1_：{}".format(hex(x1_)[2:]))
    V=mul(tB,add(PA,mul(x1_,eval(RA))))
    if V==(0,0):
        print("出错")
        sys.exit()
    (xV,yV)=V
    print("xV：{}".format(hex(xV)[2:]))
    print("yV：{}".format(hex(yV)[2:]))
    KB=KDF(hex(xV)[2:].zfill(64)+hex(yV)[2:].zfill(64)+ZA+ZB,klen)
    print("共享密钥KB：{}".format(KB))
    SB=H("02"+hex(yV)[2:].zfill(64)+H(hex(xV)[2:].zfill(64)+ZA+ZB+hex(x1)[2:].zfill(64)+hex(y1)[2:].zfill(64)+hex(x2)[2:].zfill(64)+hex(y2)[2:].zfill(64)))
    print("SB：{}".format(SB))
    print("向A发送RB和SB")
    print("RB：{}".format(RB))
    print("SB：{}".format(SB))
    s.send(str(RB).encode('utf-8'))
    time.sleep(1)
    s.send(SB.encode('utf-8'))
    print("发送完毕")
    
    S2=H("03"+hex(yV)[2:].zfill(64)+H(hex(xV)[2:].zfill(64)+ZA+ZB+hex(x1)[2:].zfill(64)+hex(y1)[2:].zfill(64)+hex(x2)[2:].zfill(64)+hex(y2)[2:].zfill(64)))
    print("S2：{}".format(S2))
    SA=s.recv(1024).decode('utf-8')
    print("收到SA")
    print("SA：{}".format(SA))
    
    if S2!=SA:
        print("出错")
        sys.exit()
    s.close()
    print("与A断开连接")
    
