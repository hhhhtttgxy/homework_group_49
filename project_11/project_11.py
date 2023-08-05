import hashlib
import hmac
import time
from math import ceil
from gmssl import sm2

def H(message): # sha256
    hash_message = hashlib.sha256(message)
    return hash_message.hexdigest()

def HMAC_K(k,m):
    k=bytes.fromhex(k)
    m=bytes.fromhex(m)
    return hmac.new(k,m,'sha256').hexdigest()

def RFC6979_gen_k(m,x,q):
    h1=H(m) #a
    h_len=len(h1)*4
    V='01'*(ceil(h_len/8)) #b
    K='00'*(ceil(h_len/8)) #c
    K=HMAC_K(K,V+'00'+x+h1) #d
    V=HMAC_K(K,V) #e
    K=HMAC_K(K,V+'01'+x+h1) #f
    V=HMAC_K(K,V) #g
    while True: #h
        T=''
        while len(T)<64:
            V=HMAC_K(K,V)
            T=T+V
        k=int(T,16)
        if 0<k<int(q,16):
            return hex(k)[2:].zfill(64)
        K=HMAC_K(K,V+'00')
        V=HMAC_K(K,V)

if __name__ == '__main__':
    private_key='00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key='B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    n="FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123"
    m=b'Hello Friend'
    start_time = time.time()
    k=RFC6979_gen_k(m,private_key,n)
    end_time = time.time()
    print("生成k用时：{}秒".format(end_time - start_time))
    print("k：",k)
    sign=sm2.CryptSM2(public_key="",private_key=private_key).sign(m,k)
    print("签名：",sign)
    if sm2.CryptSM2(public_key=public_key,private_key="").verify(sign,m):
        print("签名通过")
    else:
        print("签名未通过")
