# 这是使用自己编写的sm3算法进行的攻击
import time
import random
import string

IV = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e

def T(j):
    if 0 <= j <= 15:
        return 0x79cc4519
    elif 16 <= j <= 63:
        return 0x7a879d8a

def FF(j, X, Y, Z):
    if 0 <= j <= 15:
        result = X ^ Y ^ Z
        return result
    elif 16 <= j <= 63:
        result = (X & Y) | (X & Z) | (Y & Z)
        return result

def GG(j, X, Y, Z):
    if 0 <= j <= 15:
        result = X ^ Y ^ Z
        return result
    elif 16 <= j <= 63:
        X_f = X ^ 0xffffffff
        result = (X & Y) | (X_f & Z)
        return result

def shift_left(X, n):
    if n > 32:
        n = n - 32
    result = ((X << n) | (X >> (32 - n))) & 0xffffffff
    return result

def P0(X):
    result = X ^ shift_left(X, 9) ^ shift_left(X, 17)
    return result

def P1(X):
    result = X ^ shift_left(X, 15) ^ shift_left(X, 23)
    return result

def fill_message(message,len_bit): 
    k = (448 - 1 - len_bit) % 512
    message = int(message, 16)
    message = (message << 1) | 1
    message = (message << (k + 64)) | len_bit
    len_new = len_bit + 65 + k
    return message, len_new

def expandm(B):
    W = [0] * 68
    W_ = [0] * 64
    for i in range(16):
        W[i] = (B>>(16-1-i)*32) & 0xffffffff
    for j in range(16, 68):
        X = W[j-16] ^ W[j-9] ^ shift_left(W[j-3], 15)
        W[j] = P1(X) ^ shift_left(W[j-13], 7) ^ W[j-6]
    for j in range(64):
        W_[j] = W[j] ^ W[j+4]

    return W, W_

def CF(V, Bi):
    W, W_ = expandm(Bi)
    A = (V>>224) & 0xffffffff
    B = (V>>192) & 0xffffffff
    C = (V>>160) & 0xffffffff
    D = (V>>128) & 0xffffffff
    E = (V>>96) & 0xffffffff
    F = (V>>64) & 0xffffffff
    G = (V>>32) & 0xffffffff
    H = V & 0xffffffff
    for j in range(64):
        SS1 = shift_left((shift_left(A, 12) + E + shift_left(T(j), j))%(2**32), 7)
        SS2 = SS1 ^ shift_left(A, 12)
        TT1 = (FF(j, A, B, C) + D + SS2 + W_[j])%(2**32)
        TT2 = (GG(j, E, F, G) + H + SS1 + W[j])%(2**32)
        D, C, B, A, H, G, F, E = (C , shift_left(B, 9) , A , TT1 , G , shift_left(F, 19) , E , P0(TT2))
    return ((A << 224) | (B << 192) | (C << 160) | (D << 128) | (E << 96) | (F << 64) | (G << 32) | H) ^ V

def iteration(message_fill, n, V):
    for i in range(n):
        V[i+1]=CF(V[i], (message_fill>>(n-1-i)*512)&0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
    return V[n]

def h_sm3(message):
    message=message.encode()
    message=message.hex()
    len_bit = len(message) * 4
    message, len_new = fill_message(message,len_bit)
    n = len_new // 512
    V = [0] * (n + 1)
    V[0] = IV
    return hex(iteration(message, n, V))[2:].zfill(64)

def generate_random_string(str_length): #生成固定长度字符串
    all_str=string.ascii_letters + string.digits
    result=''.join(random.choice(all_str) for _ in range(str_length))
    return result

def birthday_attack(str_length,collision_length):
    collision_dict={}
    collision_bit_length=collision_length*4
    is_find=False
    for i in range(2**int(collision_bit_length/2)):
        str_=generate_random_string(str_length)
        hash_=h_sm3(str_)
        hash_f=hash_[:collision_length]
        if hash_f in collision_dict and collision_dict[hash_f]!=str_:
            is_find=True
            print("***找到碰撞***")
            print("碰撞前{}位：{}\n碰撞的字符串：{}\t{}".format(collision_bit_length,hash_f,str_,collision_dict[hash_f]))
            print("碰撞的哈希值：{}\t{}".format(hash_,h_sm3(collision_dict[hash_f])))
            break
        else:
            collision_dict[hash_f]=str_
    if is_find==False:
        print("***未找到***")
        
if __name__ == '__main__':
    start_time = time.time()
    birthday_attack(16,6)
    end_time = time.time()
    print("用时：{}秒".format(end_time - start_time))
