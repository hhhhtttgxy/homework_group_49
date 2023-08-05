import hashlib
import hmac
import time
import random
from math import ceil
from gmssl import sm3,func

n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
G=(0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0)
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93

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

def H(message): # sha256
    hash_message = hashlib.sha256(message)
    return hash_message.hexdigest()

def h(str_): #sm3
    data=bytes.fromhex(str_)
    hash_=sm3.sm3_hash(func.bytes_to_list(data))
    return hash_

def HMAC_K(k,m):
    k=bytes.fromhex(k)
    m=bytes.fromhex(m)
    return hmac.new(k,m,'sha256').hexdigest()

def sm2_sign(M,ID,P,d,k):
    ENTL=hex(len(ID.hex())*4)[2:].zfill(4)
    Z=h(ENTL+ID.hex()+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(P[0])[2:].zfill(64)+hex(P[1])[2:].zfill(64))
    M_=Z+M.hex()
    e=h(M_)
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
    Z=h(ENTL+ID.hex()+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(P[0])[2:].zfill(64)+hex(P[1])[2:].zfill(64))
    M__=Z+M_.hex()
    e_=h(M__)
    t=(r_+s_)%n
    if t==0:
        print("出错")
        return
    (x1_,y1_)=add(mul(s_,G),mul(t,P))
    R=(int(e_,16)+x1_)%n
    return R==r_

def RFC6979_gen_k(m,x,q):
    h1=H(m) #a
    h_len=len(h1)*4
    V='01'*(ceil(h_len/8)) #b
    K='00'*(ceil(h_len/8)) #c
    K=HMAC_K(K,V+'00'+hex(x)[2:].zfill(64)+h1) #d
    V=HMAC_K(K,V) #e
    K=HMAC_K(K,V+'01'+hex(x)[2:].zfill(64)+h1) #f
    V=HMAC_K(K,V) #g
    while True: #h
        T=''
        while len(T)<64:
            V=HMAC_K(K,V)
            T=T+V
        k=int(T,16)
        if 0<k<q:
            return k
        K=HMAC_K(K,V+'00')
        V=HMAC_K(K,V)

if __name__ == '__main__':
    d=0xB9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5
    P=(0xB9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A8308,0x1A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207)
    M=b'Hello Friend'
    ID=b"ID"
    start_time = time.time()
    k=RFC6979_gen_k(M,d,n)
    print("k：",k)
    sign=sm2_sign(M,ID,P,d,k)
    print("签名：",sign)
    if sm2_verify(M,ID,sign,P):
        print("签名通过")
    else:
        print("签名未通过")
    end_time = time.time()
    print("完整实现用时：{}秒".format(end_time - start_time))
