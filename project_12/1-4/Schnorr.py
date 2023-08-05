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

if __name__ == "__main__":
    M=b"Hello Friend!"
    start_time = time.time()
    d,P=Schnorr_keygenerate()
    R,s=Schnorr_sign(M,d)
    print("R：{}".format(R))
    print("s：{}".format(s))
    if Schnorr_verify(M,R,s,P):
        print("签名验证通过")
    else:
        print("签名验证失败")
    end_time = time.time()
    print("完整实现用时：{}秒".format(end_time - start_time))
