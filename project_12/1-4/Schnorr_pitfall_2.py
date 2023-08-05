import time
import random
from func import *

n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
G=(0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0)
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

def Schnorr_keygenerate():
    d=random.randint(1,n-1)
    P=mul(d,G)
    return d,P

def Schnorr_sign(M,d):
    k=random.randint(1,n-1)
    R=mul(k,G)
    e=H(hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M.hex())
    s=(k+int(e,16)*d)%n
    return R,s

def Schnorr_verify(M,R,s,P):
    e=H(hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M.hex())
    return mul(s,G)==add(R,mul(int(e,16),P))

#2
def Schnorr_sign_2(M,d,k):
    R=mul(k,G)
    e=H(hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M.hex())
    s=(k+int(e,16)*d)%n
    return R,s

def Schnorr_pitfall_2(M1,M2,R,s1,s2):
    e1=H(hex(R1[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M1.hex())
    e2=H(hex(R2[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M2.hex())
    d_=(inverse_mod(int(e1,16)-int(e2,16),n)*(s1-s2))%n
    return d_

if __name__ == "__main__":
    M1=b"Hello Friend!"
    M2=b"Hi Bro"
    d,P=Schnorr_keygenerate()
    print("私钥：{}".format(d))
    k=random.randint(1,n-1)
    R1,s1=Schnorr_sign_2(M1,d,k)
    R2,s2=Schnorr_sign_2(M2,d,k)
    start_time = time.time()
    d_=Schnorr_pitfall_2(M1,M2,R1,s1,s2)
    end_time = time.time()
    print("解出的私钥：{}".format(d_))
    if d_==d:
        print("一致")
    print("用时：{}秒".format(end_time - start_time))
