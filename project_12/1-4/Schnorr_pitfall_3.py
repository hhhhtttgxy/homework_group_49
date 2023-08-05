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

#3
def Schnorr_sign_3(M,d,k):
    R=mul(k,G)
    e=H(hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M.hex())
    s=(k+int(e,16)*d)%n
    return R,s

def Schnorr_pitfall_3(M,R,s,k):
    e=H(hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M.hex())
    d_=(inverse_mod(int(e,16),n)*(s-k))%n
    return d_

if __name__ == "__main__":
    M1=b"Hello Friend!"
    M2=b"Hi Bro"
    d1,P1=Schnorr_keygenerate()
    d2,P2=Schnorr_keygenerate()
    print("用户1私钥：{}".format(d1))
    print("用户2私钥：{}".format(d2))
    k=random.randint(1,n-1)
    R1,s1=Schnorr_sign_3(M1,d1,k)
    R2,s2=Schnorr_sign_3(M2,d2,k)
    start_time = time.time()
    d1_=Schnorr_pitfall_3(M1,R1,s1,k)
    d2_=Schnorr_pitfall_3(M2,R2,s2,k)
    end_time = time.time()
    print("用户2解出的用户1私钥：{}".format(d1_))
    print("用户1解出的用户2私钥：{}".format(d2_))
    if d1_==d1 and d2_==d2:
        print("一致")
    print("用时：{}秒".format(end_time - start_time))
