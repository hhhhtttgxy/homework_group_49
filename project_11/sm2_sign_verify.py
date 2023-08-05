from gmssl import sm3,func
import random

p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
G=(0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D,0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2)
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7

P=(0x0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF2548A,0x7C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857)
d=0x128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263

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

def H(str_): #sm3
    data=bytes.fromhex(str_)
    hash_=sm3.sm3_hash(func.bytes_to_list(data))
    return hash_

def sm2_sign(M, ID, P, d):
    ENTL=hex(len(ID)*4)[2:].zfill(4)
    Z=H(ENTL+ID+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(P[0])[2:].zfill(64)+hex(P[1])[2:].zfill(64))
    print("签名各步骤中的有关值：")
    print("Z：{}".format(Z))
    M_=Z+M
    print("M_：{}".format(M_))
    e=H(M_)
    print("e：{}".format(e))
    #k=random.randint(1,n-1)
    k=0x6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F # 用于验证
    (x1,y1)=mul(k,G)
    print("x1：{}".format(hex(x1)[2:]))
    print("y1：{}".format(hex(y1)[2:]))
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
    ENTL=hex(len(ID)*4)[2:].zfill(4)
    Z=H(ENTL+ID+hex(a)[2:].zfill(64)+hex(b)[2:].zfill(64)+hex(G[0])[2:].zfill(64)+hex(G[1])[2:].zfill(64)+hex(P[0])[2:].zfill(64)+hex(P[1])[2:].zfill(64))
    M__=Z+M_
    e_=H(M__)
    print("验证各步骤中的有关值：")
    print("e_：{}".format(e_))
    t=(r_+s_)%n
    print("t：{}".format(hex(t)[2:]))
    if t==0:
        print("出错")
        return
    (x1_,y1_)=add(mul(s_,G),mul(t,P))
    print("x1_：{}".format(hex(x1_)[2:]))
    print("y1_：{}".format(hex(y1_)[2:]))
    R=(int(e_,16)+x1_)%n
    print("R：{}".format(hex(R)[2:]))
    return R==r_
    
if __name__ == '__main__':
    M="6D65737361676520646967657374"
    ID="414C494345313233405941484F4F2E434F4D"
    
    sign=sm2_sign(M, ID, P, d)
    r,s=sign
    print("r：{}".format(hex(r)[2:]))
    print("s：{}".format(hex(s)[2:]))
    if sm2_verify(M,ID,sign,P):
        print("验证成功")
    else:
        print("验证失败")
