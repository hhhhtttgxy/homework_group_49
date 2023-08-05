# 实现SHA256算法
## 1. 实现过程
参照博客中的流程完成实现
https://blog.csdn.net/u013073067/article/details/86600777
## 2. 实现验证
- 参考博客中的示例进行验证
  
![image](https://github.com/hhhhtttgxy/homework_readme/assets/132645676/901113fd-8720-47ee-a42e-26a0024b4991)

![image](https://github.com/hhhhtttgxy/homework_readme/assets/132645676/f8f82483-eac8-451c-b371-a16f5bdc1cf3)

![image](https://github.com/hhhhtttgxy/homework_readme/assets/132645676/41184b29-87a4-4714-a4b4-1e0dedeed91e)

- 使用hashlib库进行验证
使用如下代码进行验证：
```python
import hashlib
import time

def sha_256(message):
    hash_message = hashlib.sha256(bytes.fromhex(message))
    return hash_message.hexdigest()

if __name__ == '__main__':
    m="61626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364616263646162636461626364"
    start_time = time.time()
    print(sha_256(m))
    end_time = time.time()
    print("用时：{}秒".format(end_time - start_time))
```

![image](https://github.com/hhhhtttgxy/homework_readme/assets/132645676/b8cdb774-7e5a-4b76-a164-95016c6b1396)
