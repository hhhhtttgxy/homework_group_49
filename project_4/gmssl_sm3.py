from gmssl import sm3,func
import time

def h(str_): #sm3
    data=bytes.fromhex(str_)
    hash_=sm3.sm3_hash(func.bytes_to_list(data))
    return hash_

if __name__ == '__main__':
    m = "61626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364"
    start_time = time.time()
    print(h(m))
    end_time = time.time()
    print("用时：{}秒".format(end_time - start_time))
