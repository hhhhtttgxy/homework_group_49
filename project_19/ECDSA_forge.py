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

def ECDSA_recover(e,r,s): # 恢复
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

    inverse_r=inverse_mod(r,n)
    u1=(-e*inverse_r)%n
    u2=(s*inverse_r)%n
    QA=[]
    for R in lst:
        QA1=add(mul(u1,G),mul(u2,R[0]))
        QA2=add(mul(u1,G),mul(u2,R[1]))
        QA.append(QA1)
        QA.append(QA2)
        
    return QA

def ECDSA_keygenerate(): #公私钥
    dA=random.randint(1,n-1)
    QA=mul(dA,G)
    return dA,QA

def ECDSA_verify(e,r,s,QA): # 验签
    if r<1 or r>n-1 or type(r)!=int or s<1 or s>n-1 or type(s)!=int:
        return False
    inverse_s=inverse_mod(s,n)
    u1=(e*inverse_s)%n
    u2=(r*inverse_s)%n
    x1,_=add(mul(u1,G),mul(u2,QA))
    return r%n==x1%n

def ECDSA_forge_sign(QA):
    u=random.randint(1,n-1)
    v=random.randint(1,n-1)
    R_=add(mul(u,G),mul(v,QA))
    (x_,y_)=R_
    r_=x_%n
    e_=(r_*u*inverse_mod(v,n))%n
    s_=(r_*inverse_mod(v,n))%n
    return e_,(r_,s_)

if __name__ == "__main__":
    start_time = time.time()
    dA,QA=ECDSA_keygenerate()
    e,sign=ECDSA_forge_sign(QA)
    r,s=sign
    print("e：{}".format(e))
    print("r：{}".format(r))
    print("s：{}".format(s))
    if ECDSA_verify(e,r,s,QA):
        print("伪造签名验证通过")
    else:
        print("伪造签名验证失败")
    end_time = time.time()
    print("伪造签名完整实现用时：{}秒".format(end_time - start_time))
    
    e_=0xd0f756e2d96f49b32579bd9365fde07674629dcab236fd9af8c01085a0cf9201
    r_=0x99cc0d1f4ed3f1e6d18c130df22fece489b4ab016c33ed53db1ce45880bf4e99
    s_=0x6633f2e0b12c0e192e73ecf20dd0131a30fa31e54314b2e7e4b57a344f76f2a8
    
    start_time1 = time.time()
    QA1,QA2=ECDSA_recover(e_,r_,s_)
    
    print("QA1：",QA1) # 恢复中本聪公钥
    print("QA2：",QA2)
    
    if ECDSA_verify(e_,r_,s_,QA1):
        print("公钥为QA1，签名验证通过")
    else:
        print("公钥为QA1，签名验证失败")
    
    if ECDSA_verify(e_,r_,s_,QA2):
        print("公钥为QA2，签名验证通过")
    else:
        print("公钥为QA2，签名验证失败")

    end_time1 = time.time()
    print("公钥恢复完整实现用时：{}秒".format(end_time1 - start_time1))

    start_time2 = time.time()
    
    e1,sign1=ECDSA_forge_sign(QA1)
    e2,sign2=ECDSA_forge_sign(QA2)
    r1,s1=sign1
    r2,s2=sign2
    print("e1：{}".format(e1))
    print("r1：{}".format(r1))
    print("s1：{}".format(s1))
    print("e2：{}".format(e2))
    print("r2：{}".format(r2))
    print("s2：{}".format(s2))
    
    if ECDSA_verify(e1,r1,s1,QA1):
        print("公钥为QA1，伪造签名验证通过")
    else:
        print("公钥为QA1，伪造签名验证失败")
    
    if ECDSA_verify(e2,r2,s2,QA2):
        print("公钥为QA2，伪造签名验证通过")
    else:
        print("公钥为QA2，伪造签名验证失败")
        
    end_time2 = time.time()
    print("伪造中本聪签名完整实现用时：{}秒".format(end_time2 - start_time2))


