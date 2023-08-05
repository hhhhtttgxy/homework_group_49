# 基础版
import base64
import binascii
import secrets
import time
from gmssl import sm2, func
from gmssl import sm3, func

def SM2_sign(data,sk):
    sm2_crypt = sm2.CryptSM2(public_key="", private_key=sk)
    random_hex_str = func.random_hex(sm2_crypt.para_len)
    sign = sm2_crypt.sign(data, random_hex_str) #  16进制
    return sign

def SM2_verify(sign,data,vk):
    sm2_crypt = sm2.CryptSM2(public_key=vk, private_key="")
    return sm2_crypt.verify(sign, data)

def SM3(data):
    data=bytes.fromhex(data)
    hash_=sm3.sm3_hash(func.bytes_to_list(data))
    return hash_

def Issuer():
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    seed = secrets.randbits(128)
    s = SM3(hex(seed)[2:].zfill(32))
    c = s
    k = 2100 - 1978
    for i in range(k):
        c = SM3(c)
    sig_c = SM2_sign(bytes.fromhex(c),private_key)
    return s, sig_c

def Alice(s, sig_c):
    d0 = 2000 - 1978
    for i in range(d0):
        s = SM3(s)
    p = s
    return p, sig_c

def Bob(p, sig_c):
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    d1 = 2100 - 2000
    for i in range(d1):
        p = SM3(p)
    c_ = p
    return SM2_verify(sig_c, bytes.fromhex(c_),public_key)

if __name__ == '__main__':
    start_time = time.time()
    s, sig_c = Issuer()
    p, sig_c = Alice(s, sig_c)
    if Bob(p, sig_c):
        print("验证成功")
    else:
        print("验证失败")
    end_time = time.time()
    print("用时：{}秒".format(end_time - start_time))
