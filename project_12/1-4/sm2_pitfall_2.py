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

#2
def sm2_sign_2(M,ID,P,d,k):
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
        
def sm2_pitfall_2(sign1,sign2):
    r1,s1=sign1
    r2,s2=sign2
    d_=(inverse_mod(s1-s2+r1-r2,n)*(s2-s1))%n
    return d_

if __name__ == '__main__':
    M1=b"Hello Friend"
    M2=b"Hi Bro"
    ID=b"ID"
    d,P=sm2_keygenerate()
    print("私钥：{}".format(d))
    k=random.randint(1,n-1)
    sign1=sm2_sign_2(M1,ID,P,d,k)
    sign2=sm2_sign_2(M2,ID,P,d,k)
    start_time = time.time()
    d_=sm2_pitfall_2(sign1,sign2)
    end_time = time.time()
    print("解出的私钥：{}".format(d_))
    if d_==d:
        print("一致")
    print("用时：{}秒".format(end_time - start_time))
