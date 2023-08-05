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

def generate_random_message(num): # 生成num个消息
    characters = "0123456789abcdef"
    test_data = [''.join(random.choices(characters, k=8)) for _ in range(num)]
    return test_data

def Schnorr_sign_(num): # 多次签名
    lst_M=generate_random_message(num)
    lst_P=[];lst_R=[];lst_s=[]
    for i in range(num):
        di,Pi=Schnorr_keygenerate()
        lst_P.append(Pi)
        Ri,si=Schnorr_sign(lst_M[i],Pi,di)
        lst_R.append(Ri)
        lst_s.append(si)
    return lst_M,lst_P,lst_R,lst_s
    
def Schnorr_batch_verify(lst_M,lst_R,lst_s,lst_P,num):
    lst_e=[]
    for i in range(num): # 计算哈希值
        ei=H(hex(lst_P[i][0])[2:].zfill(64)+hex(lst_P[i][1])[2:].zfill(64)+hex(lst_R[i][0])[2:].zfill(64)+hex(lst_R[i][1])[2:].zfill(64)+lst_M[i])
        lst_e.append(int(ei,16))
        
    s_all=(sum(lst_s))%n
    R_all=(0,0)
    eP_all=(0,0)
    for i in range(num):
        R_all=add(R_all,lst_R[i])
        eiPi=mul(lst_e[i],lst_P[i])
        eP_all=add(eP_all,eiPi)
        
    return mul(s_all,G)==add(R_all,eP_all)

if __name__ == "__main__":
    num=int(input("消息个数："))
    M,P,R,s=Schnorr_sign_(num)
    
    start_time = time.time()
    if Schnorr_batch_verify(M,R,s,P,num):
        print("批量验证通过")
    else:
        print("批量验证失败")
    end_time = time.time()
    print("验证用时：{}秒".format(end_time - start_time))
