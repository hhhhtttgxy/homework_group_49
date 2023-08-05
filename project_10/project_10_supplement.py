import time
import hashlib
import random

n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G=(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
a=0
b=7

def sha_256(message):
    hash_message = hashlib.sha256(message.encode())
    return int(hash_message.hexdigest(),16)

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

def ECDSA_keygenerate(): #公私钥
    dA=random.randint(1,n-1)
    QA=mul(dA,G)
    return dA,QA
    
def ECDSA_sign(m,dA): # 签名
    z=sha_256(m)
    while True:
        k=random.randint(1,n-1)
        x1,_=mul(k,G)
        r=x1%n
        s=(inverse_mod(k,n)*(z+r*dA))%n
        if r!=0 and s!=0:
            return r,s

def ECDSA_verify(m,r,s,QA): # 验签
    if r<1 or r>n-1 or type(r)!=int or s<1 or s>n-1 or type(s)!=int:
        return False
    z=sha_256(m)
    inverse_s=inverse_mod(s,n)
    u1=(z*inverse_s)%n
    u2=(r*inverse_s)%n
    x1,_=add(mul(u1,G),mul(u2,QA))
    return r%n==x1%n

def ECDSA_recover(m,r,s): # 恢复
    if r<1 or r>n-1 or type(r)!=int or s<1 or s>n-1 or type(s)!=int:
        return
    lst=[]
    x1=r
    while True:
        if x1>=p:
            break
        result=(pow(x1,3)+a*x1+b)%p
        if is_quadratic_residue(result,p): 
            y1_1 = quadratic_residue(result, p)
            y1_2 = (-y1_1)%p
            R1=(x1,y1_1)
            R2=(x1,y1_2)
            lst.append([R1,R2])
        x1=x1+n

    z=sha_256(m)
    inverse_r=inverse_mod(r,n)
    u1=(-z*inverse_r)%n
    u2=(s*inverse_r)%n
    QA=[]
    for R in lst:
        QA1=add(mul(u1,G),mul(u2,R[0]))
        QA2=add(mul(u1,G),mul(u2,R[1]))
        QA.append(QA1)
        QA.append(QA2)
        
    return QA

if __name__ == "__main__":
    m="Hello Friend!"
    start_time = time.time()
    dA,QA=ECDSA_keygenerate()
    r,s=ECDSA_sign(m,dA)
    print("公钥",QA)
    if ECDSA_verify(m,r,s,QA):
        print("签名验证通过")
    else:
        print("签名验证失败")
    QA_=ECDSA_recover(m,r,s)
    print("公钥恢复：",QA_)
    end_time = time.time()
    print("完整实现用时：{}秒".format(end_time - start_time))
