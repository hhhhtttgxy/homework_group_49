import hashlib
import time
import random

class Node:
    def __init__(self, hash_value, left=None, right=None, parent=None):
        self.hash = hash_value
        self.left = left
        self.right = right
        self.parent = parent

def sha_256(message):
    hash_message = hashlib.sha256(bytes.fromhex(message))
    return hash_message.hexdigest()

def create_tree(data_list):
    nodes = []

    leaf_nodes = []
    for data in data_list:
        hash_value = sha_256("00"+data)
        node = Node(hash_value)
        leaf_nodes.append(node)
    nodes.append(leaf_nodes)

    while len(nodes[-1]) != 1:
        parent_nodes = []
      
        length = len(nodes[-1])
        if length % 2:
            nodes[-1].append(nodes[-1][-1])
        
        for i in range(0, length, 2):
            parent_hash = sha_256("01"+nodes[-1][i].hash + nodes[-1][i + 1].hash)
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
    hash_value = sha_256("00"+v)
    print("验证节点的哈希值：{}".format(hash_value))
    node = None

    for leaf_node in nodes[0]:
        if leaf_node.hash == hash_value:
            node = leaf_node
            break

    if node is None:
        print("该节点验证失败")
        return

    while node.parent is not None:
        if node.parent.left == node:
            print("当前为左节点\t右节点存储的哈希值：{}".format(node.parent.right.hash))
            hash_value = sha_256("01"+hash_value + node.parent.right.hash)
        else:
            print("当前为右节点\t左节点存储的哈希值：{}".format(node.parent.left.hash))
            hash_value = sha_256("01"+node.parent.left.hash + hash_value)
            
        node = node.parent

    print("计算根节点的哈希值：{}".format(hash_value))
    
    if hash_value == root:
        print("与存储的根节点哈希值一致，该节点验证成功")
    else:
        print("该节点验证失败")

if __name__ == "__main__":
    characters = "0123456789abcdef"
    test_data = [''.join(random.choices(characters, k=8)) for _ in range(100000)] # 生成10w条数据
    print("已生成10w条数据，其中5条数据为：{}".format(test_data[50000:50005]))
    start_time = time.time()
    root, nodes = create_tree(test_data)
    end_time = time.time()
    print("建树用时：{}秒".format(end_time - start_time))
    
    print("*******Merkle树构建完成*******")
    print("根节点的哈希值：{}".format(root))
    
    print("****Merkle证明****")
    while True:
        v=input("输入想验证的节点(q结束)：")
        if v=="q":
            break  
        start_time = time.time()
        prove_node(v, root, nodes)
        end_time = time.time()
        print("证明用时：{}秒".format(end_time - start_time))

    print("****Merkle证明结束****")
