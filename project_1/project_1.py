# 这是使用gmssl库的sm3算法进行的攻击
from gmssl import sm3,func
import random
import string
import time

def h(str_): #sm3
    data=str_.encode()
    hash_=sm3.sm3_hash(func.bytes_to_list(data))
    return hash_

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
        hash_=h(str_)
        hash_f=hash_[:collision_length]
        if hash_f in collision_dict and collision_dict[hash_f]!=str_:
            is_find=True
            print("***找到碰撞***")
            print("碰撞前{}位：{}\n碰撞的字符串：{}\t{}".format(collision_bit_length,hash_f,str_,collision_dict[hash_f]))
            print("碰撞的哈希值：{}\t{}".format(hash_,h(collision_dict[hash_f])))
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
