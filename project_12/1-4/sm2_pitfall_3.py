import time
import random
from func import *

n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
G=(0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0)
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

def sm2_keygenerate():
    d=random.randint(1,n-1)
    P=mul(d,G)
    return d,P

def sm2_sign(M,ID,P,d):
    ENTL=hex(len(ID.hex())*4)[2:].zfill(4)
    Z=H(ENTL+ID.hex()+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(P[0])[2:].zfill(64)+hex(P[1])[2:].zfill(64))
    M_=Z+M.hex()
    e=H(M_)
    k=random.randint(1,n-1)
    (x1,y1)=mul(k,G)
    r=(int(e,16)+x1)%n
    if r==0 or r+k==n:
        print("出错")
        return
    s=(inverse_mod(1+d,n)*(k-r*d))%n
    if s==0:
        print("出错")
        return
    return (r,s)
    
def sm2_verify(M_,ID,sign,P):
    r_,s_=sign
    if r_<1 or r_>n-1 or s_<1 or s_>n-1:
        print("出错")
        return
    ENTL=hex(len(ID.hex())*4)[2:].zfill(4)
    Z=H(ENTL+ID.hex()+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(P[0])[2:].zfill(64)+hex(P[1])[2:].zfill(64))
    M__=Z+M_.hex()
    e_=H(M__)
    t=(r_+s_)%n
    if t==0:
        print("出错")
        return
    (x1_,y1_)=add(mul(s_,G),mul(t,P))
    R=(int(e_,16)+x1_)%n
    return R==r_

#3
def sm2_sign_3(M,ID,P,d,k):
    ENTL=hex(len(ID.hex())*4)[2:].zfill(4)
    Z=H(ENTL+ID.hex()+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(P[0])[2:].zfill(64)+hex(P[1])[2:].zfill(64))
    M_=Z+M.hex()
    e=H(M_)
    (x1,y1)=mul(k,G)
    r=(int(e,16)+x1)%n
    if r==0 or r+k==n:
        print("出错")
        return
    s=(inverse_mod(1+d,n)*(k-r*d))%n
    if s==0:
        print("出错")
        return
    return (r,s)
        
def sm2_pitfall_3(sign,k):
    r,s=sign
    d_=(inverse_mod(s+r,n)*(k-s))%n
    return d_

if __name__ == '__main__':
    M1=b"Hello Friend"
    M2=b"Hi Bro"
    ID1=b"ID1"
    ID2=b"ID2"
    d1,P1=sm2_keygenerate()
    d2,P2=sm2_keygenerate()
    print("用户1私钥：{}".format(d1))
    print("用户2私钥：{}".format(d2))
    k=random.randint(1,n-1)
    sign1=sm2_sign_3(M1,ID1,P1,d1,k)
    sign2=sm2_sign_3(M2,ID2,P2,d2,k)
    start_time = time.time()
    d1_=sm2_pitfall_3(sign1,k)
    d2_=sm2_pitfall_3(sign2,k)
    end_time = time.time()
    print("用户2解出的用户1私钥：{}".format(d1_))
    print("用户1解出的用户2私钥：{}".format(d2_))
    if d1==d1_ and d2==d2_:
        print("一致")
    print("用时：{}秒".format(end_time - start_time))
