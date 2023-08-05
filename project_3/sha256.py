import time

h0=0x6a09e667
h1=0xbb67ae85
h2=0x3c6ef372
h3=0xa54ff53a
h4=0x510e527f
h5=0x9b05688c
h6=0x1f83d9ab
h7=0x5be0cd19
k=[
0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

def shift_right(X, n):
    result = ((X >> n) | (X << (32 - n))) & 0xffffffff
    return result

def fill_message(message,len_bit): 
    k = (448 - 1 - len_bit) % 512
    message = int(message, 16)
    message = (message << 1) | 1
    message = (message << (k + 64)) | len_bit
    len_new = len_bit + 65 + k
    return message, len_new

def expandm(B):
    w = [0] * 64
    for i in range(16):
        w[i] = (B>>(16-1-i)*32) & 0xffffffff
    for i in range(16, 64):
        s0=shift_right(w[i-15], 7)^shift_right(w[i-15], 18)^(w[i-15]>>3)
        s1=shift_right(w[i-2], 17)^shift_right(w[i-2], 19)^(w[i-2]>>10)
        w[i]=(w[i-16]+s0+w[i-7]+s1)%(2**32)
    '''
    for i in range(64):
        print(hex(w[i])[2:].zfill(8),end=' ')
    print()
    print()
    '''
    return w

def CF(V, B):
    w = expandm(B)
    h0,h1,h2,h3,h4,h5,h6,h7=V
    a=h0
    b=h1
    c=h2
    d=h3
    e=h4
    f=h5
    g=h6
    h=h7
    #print("{:2} {:08x} {:08x} {:08x} {:08x} {:08x} {:08x} {:08x} {:08x}".format(0,a,b,c,d,e,f,g,h))
    for i in range(64):
        S1=shift_right(e, 6)^shift_right(e, 11)^shift_right(e, 25)
        ch=(e&f)^((e^0xffffffff)&g)
        temp1=(h+S1+ch+k[i]+w[i])%(2**32)
        S0=shift_right(a, 2)^shift_right(a, 13)^shift_right(a,22)
        maj=(a&b)^(a&c)^(b&c)
        temp2=(S0+maj)%(2**32)
        h=g
        g=f
        f=e
        e=(d + temp1)%(2**32)
        d=c
        c=b
        b=a
        a=(temp1 + temp2)%(2**32)
        #print("{:2} {:08x} {:08x} {:08x} {:08x} {:08x} {:08x} {:08x} {:08x}".format(i+1,a,b,c,d,e,f,g,h))
    #print()
    h0=(h0 + a)%(2**32)
    h1=(h1 + b)%(2**32)
    h2=(h2 + c)%(2**32)
    h3=(h3 + d)%(2**32)
    h4=(h4 + e)%(2**32)
    h5=(h5 + f)%(2**32)
    h6=(h6 + g)%(2**32)
    h7=(h7 + h)%(2**32)
    return [h0,h1,h2,h3,h4,h5,h6,h7]

def iteration(message_fill, n, V):
    for i in range(n):
        V=CF(V, (message_fill>>(n-1-i)*512)&0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
    return V

def h_sha256(message):
    len_bit = len(message) * 4
    message, len_new = fill_message(message,len_bit)
    #print(hex(message)[2:])
    #print()
    n = len_new // 512
    V=[h0,h1,h2,h3,h4,h5,h6,h7]
    a,b,c,d,e,f,g,h=iteration(message, n, V)
    result=(a << 224) | (b << 192) | (c << 160) | (d << 128) | (e << 96) | (f << 64) | (g << 32) | h
    return hex(result)[2:].zfill(64)

if __name__ == '__main__':
    m="61626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364"
    #m="616263"
    start_time = time.time()
    print(h_sha256(m))
    end_time = time.time()
    print("用时：{}秒".format(end_time - start_time))
