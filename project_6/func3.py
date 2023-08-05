import base64
import binascii
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

