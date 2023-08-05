import time
import random

n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G=(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
a=0
b=7

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

def Schnorr_verify(e,R,s,P):
    return mul(s,G)==add(R,mul(e,P))

def Schnorr_forge_sign(P):
    e=random.randint(1,n-1)
    s=random.randint(1,n-1)
    sG=mul(s,G)
    eP=mul(e,P)
    _eP=(eP[0],p-eP[1]) # -eP
    R=add(sG,_eP)
    return e,(R,s)

if __name__ == "__main__":
    start_time = time.time()
    d,P=Schnorr_keygenerate()
    e,sign=Schnorr_forge_sign(P)
    R,s=sign
    print("e：{}".format(e))
    print("R：{}".format(R))
    print("s：{}".format(s))
    if Schnorr_verify(e,R,s,P):
        print("伪造签名验证通过")
    else:
        print("伪造签名验证失败")
    end_time = time.time()
    print("完整实现用时：{}秒".format(end_time - start_time))
