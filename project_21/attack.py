import time
import hashlib
import random

n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G=(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
a=0
b=7

def H(message): # sha256
    hash_message = hashlib.sha256(bytes.fromhex(message))
    return hash_message.hexdigest()

def gcd(m,n): # 最大公因子
    if m%n==0:
        return n
    else:
        return gcd(n,m%n)

def inverse_mod(a,m): # 模逆
    if gcd(a,m)!=1: # 若a和m不互质，则无模逆
        return None 
    x1,x2,x3=1,0,a
    y1,y2,y3=0,1,m
    while y3!=0:
        q=x3//y3 
        y1,y2,y3,x1,x2,x3=(x1-q*y1),(x2-q*y2),(x3-q*y3),y1,y2,y3
    return x1%m

def add(P,Q): # 椭圆曲线加法
    x1,y1=P
    x2,y2=Q
    if x1==y1==0:
        return (x2,y2)
    if x2==y2==0:
        return (x1,y1)
    if x1==x2:
        if y1==y2:
            n=(3*pow(x1,2)+a) # 分子
            m=(2*y1) # 分母
        else:
            return (0,0) # 无穷远点
    else:
        n=y2-y1
        m=x2-x1
        
    la=(n*inverse_mod(m,p))%p
    x3=(pow(la,2)-x1-x2)%p
    y3=(la*(x1-x3)-y1)%p
    return (x3,y3)

def double(point):
    return add(point,point)

def mul(t, point): # 快速乘
    if t==0:
        return 0
    if t==1:
        return point
    if t&1==0:
        return double(mul(t>>1, point))
    if t&1==1:
        return add(point,double(mul(t>>1, point)))

def Schnorr_keygenerate():
    d=random.randint(1,n-1)
    P=mul(d,G)
    return d,P

def Schnorr_sign(M,P,d):
    k=random.randint(1,n-1)
    R=mul(k,G)
    e=H(hex(P[0])[2:].zfill(64)+hex(P[1])[2:].zfill(64)+hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M)
    s=(k+int(e,16)*d)%n
    return R,s

def Schnorr_verify(M,R,s,P):
    e=H(hex(P[0])[2:].zfill(64)+hex(P[1])[2:].zfill(64)+hex(R[0])[2:].zfill(64)+hex(R[1])[2:].zfill(64)+M)
    return mul(s,G)==add(R,mul(int(e,16),P))

def Schnorr_verify_2(M1,M2,sign1,sign2,P1,P2):
    R1,s1=sign1
    R2,s2=sign2
    e1=H(hex(P1[0])[2:].zfill(64)+hex(P1[1])[2:].zfill(64)+hex(R1[0])[2:].zfill(64)+hex(R1[1])[2:].zfill(64)+M1.hex())
    e2=H(hex(P2[0])[2:].zfill(64)+hex(P2[1])[2:].zfill(64)+hex(R2[0])[2:].zfill(64)+hex(R2[1])[2:].zfill(64)+M2.hex())

    s=(s1+s2)%n
    R=add(R1,R2)
    eP=add(mul(int(e1,16),P1),mul(int(e2,16),P2))
        
    return mul(s,G)==add(R,eP)

def attack(M1,M2,d1,P1,P2):
    r2=random.randint(1,n-1)
    s2=random.randint(1,n-1)
    R2=mul(r2,G)
    e2=H(hex(P2[0])[2:].zfill(64)+hex(P2[1])[2:].zfill(64)+hex(R2[0])[2:].zfill(64)+hex(R2[1])[2:].zfill(64)+M2.hex())
    _R1=mul(int(e2,16),P2)
    R1=(_R1[0],p-_R1[1])
    e1=H(hex(P1[0])[2:].zfill(64)+hex(P1[1])[2:].zfill(64)+hex(R1[0])[2:].zfill(64)+hex(R1[1])[2:].zfill(64)+M1.hex())
    s1=(r2+int(e1,16)*d1-s2)%n
    return (R1,s1),(R2,s2)

if __name__ == "__main__":
    M1=b'Hello Friend'
    M2=b'Hi Bro'
    d1,P1=Schnorr_keygenerate() # 攻击者的公私钥
    d2,P2=Schnorr_keygenerate()
    start_time = time.time()
    sign1,sign2=attack(M1,M2,d1,P1,P2)
    
    if Schnorr_verify_2(M1,M2,sign1,sign2,P1,P2):
        print("伪造签名通过")
    else:
        print("伪造签名失败")
    end_time = time.time()
    print("用时：{}秒".format(end_time - start_time))
