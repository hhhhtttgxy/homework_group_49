import time
import random
from func import *

n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
G=(0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0)
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

def ECDSA_keygenerate(): #公私钥
    dA=random.randint(1,n-1)
    QA=mul(dA,G)
    return dA,QA
    
def ECDSA_sign(m,dA,k): # 签名
    z=H(m.hex())
    z=int(z,16)
    x1,_=mul(k,G)
    r=x1%n
    s=(inverse_mod(k,n)*(z+r*dA))%n
    if r!=0 and s!=0:
        return r,s

def ECDSA_verify(m,r,s,QA): # 验签
    if r<1 or r>n-1 or type(r)!=int or s<1 or s>n-1 or type(s)!=int:
        return False
    z=H(m.hex())
    z=int(z,16)
    inverse_s=inverse_mod(s,n)
    u1=(z*inverse_s)%n
    u2=(r*inverse_s)%n
    x1,_=add(mul(u1,G),mul(u2,QA))
    return r%n==x1%n

def Schnorr_keygenerate():
    d=random.randint(1,n-1)
    P=mul(d,G)
    return d,P

def Schnorr_sign(M,d,k):
    R=mul(k,G)
    e=H(hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M.hex())
    s=(k+int(e,16)*d)%n
    return R,s

def Schnorr_verify(M,R,s,P):
    e=H(hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M.hex())
    return mul(s,G)==add(R,mul(int(e,16),P))

def pitfall_7(M,r,s1,R,s2):
    e1=int(H(M.hex()),16)
    e2=int(H(hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M.hex()),16)
    d_=((s1*s2-e1)*inverse_mod(r+e2*s1,n))%n
    return d_
    
if __name__ == '__main__':
    M=b"Hello Friend"
    start_time = time.time()
    d,P=ECDSA_keygenerate() # 2种签名算法公私钥生成方式一致
    print("私钥：{}".format(d))
    k=random.randint(1,n-1)
    r,s1=ECDSA_sign(M,d,k)
    R,s2=Schnorr_sign(M,d,k)
    d_=pitfall_7(M,r,s1,R,s2)
    print("解出的私钥：{}".format(d_))
    if d_==d:
        print("一致")
    end_time = time.time()
    print("完整实现用时：{}秒".format(end_time - start_time))
