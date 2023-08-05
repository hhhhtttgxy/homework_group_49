import base64
import binascii
from gmssl import sm2, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

def sm2_enc(p,pk):
    sm2_crypt = sm2.CryptSM2(public_key=pk, private_key="")
    enc_p = sm2_crypt.encrypt(p)
    return enc_p

def sm2_dec(c,sk):
    sm2_crypt = sm2.CryptSM2(public_key="", private_key=sk)
    dec_c =sm2_crypt.decrypt(c)
    return dec_c

def sm4_enc(p,k):
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(k, SM4_ENCRYPT)
    enc_p = crypt_sm4.crypt_ecb(p)
    return enc_p

def sm4_dec(c,k):
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(k, SM4_DECRYPT)
    dec_c = crypt_sm4.crypt_ecb(c)
    return dec_c

