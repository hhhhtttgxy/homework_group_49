import time
import random

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

def sm2_keygenerate():
    d=random.randint(1,n-1)
    P=mul(d,G)
    return d,P
    
def sm2_verify(e_,sign,P):
    r_,s_=sign
    if r_<1 or r_>n-1 or s_<1 or s_>n-1:
        print("出错")
        return
    t=(r_+s_)%n
    if t==0:
        print("出错")
        return
    (x1_,y1_)=add(mul(s_,G),mul(t,P))
    R=(e_+x1_)%n
    return R==r_

def sm2_sign(P):
    u=random.randint(1,n-1)
    v=random.randint(1,n-1)
    (x1,y1)=add(mul(u,G),mul(v,P))
    s=u
    r=(v-s)%n
    e=(r-x1)%n
    return e,(r,s)
    
if __name__ == '__main__':
    start_time = time.time()
    d,P=sm2_keygenerate()
    e,sign=sm2_sign(P)
    r,s=sign
    print("e：{}".format(e))
    print("r：{}".format(r))
    print("s：{}".format(s))
    if sm2_verify(e,sign,P):
        print("伪造签名验证通过")
    else:
        print("伪造签名验证失败")
    end_time = time.time()
    print("完整实现用时：{}秒".format(end_time - start_time))
