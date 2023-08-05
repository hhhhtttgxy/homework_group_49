import random
from func9 import *

def generate_d1_d2(d,n):
    d1=random.randint(1, n-1)
    d1d2=inverse_mod(d+1,n) # d=(d1*d2)的-1次方-1
    d2=(d1d2*inverse_mod(d1,n))%n
    if (d-inverse_mod(d1*d2,n)+1)%n==0:
        return d1,d2
    else:
        return

if __name__ == '__main__':
    d=0x00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5
    n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    d1,d2=generate_d1_d2(d,n)
    print("d1：{}".format(d1))
    print("d2：{}".format(d2))
    
