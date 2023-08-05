# 这是使用gmssl库的sm3算法进行的攻击
from gmssl import sm3,func
import time

def h(str_): #sm3
    data=bytes.fromhex(str_)
    hash_=sm3.sm3_hash(func.bytes_to_list(data))
    return hash_

def rho_attack(initial_str,collision_length):
    collision_bit_length=collision_length*4
    initial1=initial_str
    initial2=initial_str
    while True:
        initial1=h(initial1)[:collision_length]
        initial2=h(h(initial2)[:collision_length])[:collision_length]
        if initial1==initial2:
            print("***找到碰撞***")
            print("碰撞前{}位：{}".format(collision_bit_length,initial1))
            break

if __name__ == '__main__':
    start_time = time.time()
    rho_attack("0123456789abcdef",6)
    end_time = time.time()
    print("用时：{}秒".format(end_time - start_time))
