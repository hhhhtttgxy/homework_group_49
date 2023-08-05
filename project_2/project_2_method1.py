# 这是使用gmssl库的sm3算法进行的攻击
from gmssl import sm3,func
import time

def h(str_): #sm3
    data=bytes.fromhex(str_)
    hash_=sm3.sm3_hash(func.bytes_to_list(data))
    return hash_

def rho_attack(initial_str,collision_length):
    attack_list=[]
    collision_bit_length=collision_length*4
    initial_hash=h(initial_str)
    initial_hash_f=initial_hash[:collision_length]
    attack_list.append(initial_hash_f)
    while True:
        initial_hash_s1=initial_hash_f
        initial_hash_s2=h(initial_hash_f)
        initial_hash_f=h(initial_hash_f)
        initial_hash_f=initial_hash_f[:collision_length]
        if initial_hash_f in attack_list:
            print("***找到碰撞***")
            print("碰撞前{}位：{}".format(collision_bit_length,initial_hash_f))
            print("碰撞的字符串：{}\t{}".format(attack_list[attack_list.index(initial_hash_f)-1],initial_hash_s1))
            print("碰撞的哈希值：{}\t{}".format(h(attack_list[attack_list.index(initial_hash_f)-1]),initial_hash_s2))
            break
        else:
            attack_list.append(initial_hash_f)

if __name__ == '__main__':
    start_time = time.time()
    rho_attack("0123456789abcdef",6)
    end_time = time.time()
    print("用时：{}秒".format(end_time - start_time))
