import time
import os
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class Node:
    def __init__(self, hash_value, left=None, right=None, parent=None):
        self.hash = hash_value
        self.left = left
        self.right = right
        self.parent = parent

def sha256(message):
    digest = hashes.Hash(hashes.SHA256())
    message = bytes.fromhex(message)
    digest.update(message)
    hash_value = digest.finalize()
    return hash_value.hex()

def create_tree(a,b,c,d):
    data_list=[0]*16
    random_list=[]
    while True: # 生成四个随机位置给a b c d
        if len(random_list)==4:
            break
        k=random.randint(0,15)
        if k not in random_list:
            random_list.append(k)
            
    index0,index1,index2,index3=random_list
    data_list[index0]=a;data_list[index1]=b;data_list[index2]=c;data_list[index3]=d
    for i in range(16):
        if i not in random_list:
            data_list[i]=sha256(os.urandom(64).hex())

    nodes = []

    leaf_nodes = []
    for data in data_list:
        node = Node(data)
        leaf_nodes.append(node)
    nodes.append(leaf_nodes)

    while len(nodes[-1]) != 1:
        parent_nodes = []
      
        length = len(nodes[-1])
        if length % 2:
            nodes[-1].append(nodes[-1][-1])
        
        for i in range(0, length, 2):
            parent_hash = sha256(nodes[-1][i].hash + nodes[-1][i + 1].hash)
            node = Node(parent_hash)
            node.left = nodes[-1][i]
            node.right = nodes[-1][i + 1]
            nodes[-1][i].parent = node
            nodes[-1][i + 1].parent = node
            parent_nodes.append(node)

        nodes.append(parent_nodes)

    root = nodes[-1][0].hash
    return root, nodes

def prove_node(v, root, nodes):
    hash_value = v
    node = None

    for leaf_node in nodes[0]:
        if leaf_node.hash == hash_value:
            node = leaf_node
            break

    if node is None:
        return False

    while node.parent is not None:
        if node.parent.left == node:
            hash_value = sha256(hash_value + node.parent.right.hash)
        else:
            hash_value = sha256(node.parent.left.hash + hash_value)
            
        node = node.parent

    return hash_value == root
    
def hkdf(key):
    key = bytes.fromhex(key)
    hkdf_i = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=os.urandom(32),
        info=b"hkdf",
    )
    subkey = hkdf_i.derive(key)
    return subkey.hex()

def pl_accum(a,b,c):
    return sha256(a+b+c)

def H(a,b):
    return sha256(a+b)

def shuffle(arr, seed):
    seed = int(seed,16)
    rng = random.Random(seed)
    rng.shuffle(arr)
    return arr

def checksum(seed_d):
    for i in range(9):
        seed_d=sha256(seed_d)
    comm_checksum=seed_d
    D=comm_checksum
    return D

def issuer(num):
    x,y,z=str(num).zfill(3)
    x=int(x);y=int(y);z=int(z)
    
    if 0<=x<=2 and 0<=y<=3 and 0<=z<=3:
        chain=233
    elif 300<=num<=303:
        chain=303
    elif 310<=num<=312:
        chain=312
        
    random_bytes = os.urandom(32)
    seed_main = random_bytes.hex()
    
    s1=hkdf(seed_main);h1_1 = sha256(s1);h1_2 = sha256(h1_1);h1_3 = sha256(h1_2)
    s2=hkdf(seed_main);h2_1 = sha256(s2);h2_2 = sha256(h2_1);h2_3 = sha256(h2_2)
    s3=hkdf(seed_main);h3_1 = sha256(s3);h3_2 = sha256(h3_1);h3_3 = sha256(h3_2)

    comm_312=pl_accum(h3_3,h2_1,h1_2)
    comm_303=pl_accum(h3_3,s2,h1_3)
    comm_233=pl_accum(h3_2,h2_3,h1_3)
    
    salt_A=hkdf(seed_main)
    salt_B=hkdf(seed_main)
    salt_C=hkdf(seed_main)
    
    if chain==233:
        salt=salt_C
    elif chain==303:
        salt=salt_B
    elif chain==312:
        salt=salt_A
        
    A=H(salt_A,comm_312)
    B=H(salt_B,comm_303)
    C=H(salt_C,comm_233)
    shuffle_seed=hkdf(seed_main)
    A,B,C=shuffle([A,B,C],shuffle_seed)
    seed_d=hkdf(seed_main)
    D=checksum(seed_d)
    root, nodes=create_tree(A,B,C,D)
    
    return s1,s2,s3,chain,salt,root,nodes

def prove(s1,s2,s3,num,chain):
    x,y,z=str(num).zfill(3)
    x=int(x);y=int(y);z=int(z)
    
    x_,y_,z_=str(chain).zfill(3)
    x_=int(x_);y_=int(y_);z_=int(z_)
    
    a=s3;b=s2;c=s1

    for i in range(x_-x):
        a=sha256(a)
    for i in range(y_-y):
        b=sha256(b)
    for i in range(z_-z):
        c=sha256(c)
        
    return a,b,c
    
def verify(a,b,c,num,salt,root,nodes):
    x,y,z=str(num).zfill(3)
    x=int(x);y=int(y);z=int(z)
    
    for i in range(x):
        a=sha256(a)
    for i in range(y):
        b=sha256(b)
    for i in range(z):
        c=sha256(c)
    comm_=pl_accum(a,b,c)
    comm_salt=H(salt,comm_)
    return prove_node(comm_salt, root, nodes)
    
if __name__ == '__main__': # HashWires
    num=int(input("请输入："))
    start_time = time.time()
    s1,s2,s3,chain,salt,root,nodes=issuer(num)
    a,b,c=prove(s1,s2,s3,num,chain)
    if verify(a,b,c,num,salt,root,nodes):
        print("验证成功")
    else:
        print("验证失败")
    end_time = time.time()
    print("用时：{}秒".format(end_time - start_time))
