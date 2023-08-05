import random
import hashlib

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

def is_quadratic_residue(a,p): # 欧拉准则
    return pow(a,(p-1)//2,p)==1 

def quadratic_residue(a,p):
    if p%4==3:
        result=pow(a,(p+1)//4,p)
        if result>p-result:
            return p-result
        return result
    
    while True: # 找到一个非二次剩余
        b=random.randint(1,p-1)
        if is_quadratic_residue(b,p)==False:
            break
    temp=p-1
    t=0
    while True:
        if temp%2!=0:
            break
        temp=temp//2
        t=t+1
    s=(p-1)//pow(2,t)

    x=[0]*t
    w=[0]*t
    x[t-1]=pow(a,(s+1)//2,p)
    w[t-1]=(inverse_mod(a,p)*pow(x[t-1],2,p))%p
    for i in range(t-1,0,-1):
        if pow(w[i],pow(2,i-1),p)==1:
            x[i-1]=x[i]
        else:
            la=pow(b,pow(2,t-i-1)*s,p)
            x[i-1]=(la*x[i])%p
            
        w[i-1]=(inverse_mod(a,p)*pow(x[i-1],2,p))%p

    if x[0]>p-x[0]:
        return p-x[0]
    
    return x[0]

def sha_256(message):
    hash_message = hashlib.sha256(message.encode())
    return hash_message.hexdigest()

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

def message_to_point(m): # Try-and-Increment Method
    h_m=sha_256(m)
    u=int(h_m,16)
    i = 0
    while True:
        x=(u+i)%p
        temp=(pow(x,3)+a*x+b)%p
        if is_quadratic_residue(temp,p): 
            y = quadratic_residue(temp, p)
            Q=(x, y)
            return Q
        i+=1

def ECMH_add(m,ECMH): # 添加
    ECMH_m=message_to_point(m)
    result=add(ECMH,ECMH_m)
    return result


def ECMH_delete(m,ECMH): # 删除
    ECMH_m=message_to_point(m)
    _ECMH_m=(ECMH_m[0],p-ECMH_m[1]) # -ECMH_m
    result=add(ECMH,_ECMH_m)
    return result

if __name__ == '__main__':
    m1="message1"
    m2="message2"
    m3="message3"
    
    print("*******添加功能*******")
    ECMH=(0,0)
    ECMH=ECMH_add(m1,ECMH)
    print("ECMH(m1)：{}".format(ECMH))
    ECMH=ECMH_add(m2,ECMH)
    print("ECMH(m1,m2)：{}".format(ECMH))
    ECMH=ECMH_add(m3,ECMH)
    print("ECMH(m1,m2,m3)：{}".format(ECMH))
    
    print("*******删除功能*******")
    ECMH=ECMH_delete(m2,ECMH)
    print("ECMH(m1,m2,m3)-ECMH(m2)：{}".format(ECMH))
    ECMH_1=(0,0) # 用于验证
    ECMH_1=ECMH_add(m1,ECMH_1)
    ECMH_1=ECMH_add(m3,ECMH_1)
    print("ECMH(m1,m3)：{}".format(ECMH_1))
    
    m4="message4"
    m5="message5"

    print("********交换律********")
    ECMH_2=(0,0)
    ECMH_2=ECMH_add(m4,ECMH_2)
    ECMH_2=ECMH_add(m5,ECMH_2)
    print("ECMH(m4,m5)：{}".format(ECMH_2))

    ECMH_3=(0,0)
    ECMH_3=ECMH_add(m5,ECMH_3)
    ECMH_3=ECMH_add(m4,ECMH_3)
    print("ECMH(m5,m4)：{}".format(ECMH_3))
    
