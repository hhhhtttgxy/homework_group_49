# do your best to optimize SM3 implementation (software)
# 在软件层面上尽力优化sm3算法

|     代码名称     |           具体实现           |
| :--------------: | :--------------------------: |
|   gmssl_sm3.py   |    调用gmssl库中的sm3算法    |
|      sm3.py      |       自编写的sm3算法        |
| sm3_original.cpp |   基础实现未优化的sm3算法    |
|   sm3_best.cpp   |       已优化的sm3算法        |
|  Linux_sm3.cpp   | 准备放入Linux下优化的sm3算法 |

## 1. 基础实现过程
先实现一个基础版本的sm3算法，在project_3中已经实现了sm3算法的python版本，因此只需要略作编程语言的调整更改，由于C++大数溢出以及字符串与整数的转化较为复杂等原因，因此在C++中将部分函数合并且不使用字符串，由于后续需要进行优化，因此在编写代码的过程中对于一些明显的、容易优化的且可读性与未调整差别不大的地方进行优化，例如，使用移位操作代替乘法除法。

## 2. 基础实现验证
- 第一个消息分组：

![image](./image/e9cc0335-afdd-4957-b4b3-bc6007b993f9.png)

- 第一个消息分组迭代压缩中间值（部分）：

![image](./image/cf2dd7d8-260e-41ae-8b1a-06a0edd5620e.png)

- 第二个消息分组：

![image](./image/f1696c78-be5f-45b5-9f8c-6cc4514d0b5a.png)

- 第二个消息分组迭代压缩中间值（部分）：

![image](./image/0a43fe20-0ed9-4b7f-90a0-15ecb8dca843.png)

- 最终压缩结果：

![image](./image/d7fb6c7e-d9bb-4c3e-8fc7-13e1571ada7c.png)

经验证，中间过程与结果均与官方文档一致。

## 3. 优化实现过程
主要采取三种优化方式：SIMD（一条指令处理多个数据）、UNROLL（循环展开）和INLINE（函数内联）。

### 3.1 SIMD
SIMD 的全称是 Single Instruction Multiple Data，即单指令多数据。顾名思义是一条指令处理多个数据。SIMD 本质上是采用一个控制器来控制多个处理器，同时对一组数据中的每一条分别执行相同的操作，从而实现空间上的并行性的技术，以下示例是SIMD与UNROLL的结合。

```C++
for (int j = 0; j < 64; j += 16) {
    __m256i Wj, Wj_4, Wj_, Wj_4_;
    Wj = _mm256_loadu_si256((__m256i*) & W[j]);
    Wj_4 = _mm256_loadu_si256((__m256i*) & W[j + 4]);
    Wj_ = _mm256_loadu_si256((__m256i*) & W[j + 8]);
    Wj_4_ = _mm256_loadu_si256((__m256i*) & W[j + 12]);
    _mm256_storeu_si256((__m256i*) & W_[j], _mm256_xor_si256(Wj, Wj_4));
    _mm256_storeu_si256((__m256i*) & W_[j + 8], _mm256_xor_si256(Wj_, Wj_4_));
}
```

### 3.2 UNROLL
unroll 是一种循环展开的优化技术，它可以提高代码的执行效率，循环展开有助于减少循环的迭代次数，从而减少循环的控制开销、跳转开销和循环内部的指令冲突等问题。同时，它可以增加指令级并行度，让循环体中的指令可以更好地重叠执行，从而提高程序的效率，注意在使用时，尽量保证在循环体内的运算没有关联性，以达到最大的并行性，以下给出一个示例。

```C++
for (int i = 0; i < len_fB_4; i += 4)
{
    B[i] = ((F[i * 4] << 24) | (F[i * 4 + 1] << 16) | (F[i * 4 + 2] << 8) | F[i * 4 + 3]) & 0xffffffff;
    B[i + 1] = ((F[(i + 1) * 4] << 24) | (F[(i + 1) * 4 + 1] << 16) | (F[(i + 1) * 4 + 2] << 8) | F[(i + 1) * 4 + 3]) & 0xffffffff;
    B[i + 2] = ((F[(i + 2) * 4] << 24) | (F[(i + 2) * 4 + 1] << 16) | (F[(i + 2) * 4 + 2] << 8) | F[(i + 2) * 4 + 3]) & 0xffffffff;
    B[i + 3] = ((F[(i + 3) * 4] << 24) | (F[(i + 3) * 4 + 1] << 16) | (F[(i + 3) * 4 + 2] << 8) | F[(i + 3) * 4 + 3]) & 0xffffffff;
}
```
### 3.3 INLINE
内联函数可以提高程序执行效率。如果函数是内联的，编译器在编译时，会把内联函数的实现替换到每个调用内联函数的地方。
```C++
inline unsigned int T(int j)
```

> 注：后补充在Linux下使用SIMD和O3完成优化（直接放入C++基础实现代码即可），编译指令如下，由于之前的测量时间方法只能在Windows下使用，故更改了测量时间的方法（如下）。

```
g++ -mavx -O3 -o sm3 sm3.cpp
```

```C++
auto start = chrono::high_resolution_clock::now();
int len_byte = sizeof(message) / sizeof(message[0]);
sm3(message, len_byte);
auto end = chrono::high_resolution_clock::now();
auto duration = chrono::duration_cast<chrono::microseconds>(end - start);
cout << "用时：" << duration.count() << " 微秒" << endl;
```

## 3. 实现效率对比
- 五个版本每个版本测量5次，取平均值，以下时间单位均为秒（s），Linux下的优化单位除外，为微秒。

> gmssl版本的运行效率：
> 
> ![image](./image/4d10a241-ee40-4fde-b236-57af248c146b.png)
>
> ![image](./image/a91b4a99-37e9-44a3-9c57-d5e7ad3c2481.png)
>
> ![image](./image/508b7cda-6d62-4bc5-9f9e-8864001a7b48.png)
>
> ![image](./image/16166372-c46a-46da-aded-1336efed8a8c.png)
>
> ![image](./image/4858dade-173e-4b21-9df9-f76d0ccb7eed.png)


> python版本的运行效率：
>
> ![image](./image/65b97991-1589-4b02-a33d-cbc4d9becec7.png)
>
> ![image](./image/405b4768-f022-43bd-b617-dc89bdd0c017.png)
> 
> ![image](./image/993e9fe3-0ce1-4788-81ea-bb77528897fa.png)
>
> ![image](./image/9a5bec6b-4632-4c29-a6b1-ddc53534a206.png)
> 
> ![image](./image/d4482d7a-9f5e-4b91-b471-d669baa044ff.png)


> C++初步实现未优化版本的运行效率：
>
> ![image](./image/48e76a0f-8395-4770-8a33-001c8c80e1c4.png)
> 
> ![image](./image/a8e8c6c6-4f5b-414d-84fb-f045ec1c0f36.png)
>
> ![image](./image/e53ebb92-f192-4c90-b053-d477679db8c8.png)
>
> ![image](./image/8c3758dd-dc5e-4d03-a0c8-eebb19efae24.png)
>
> ![image](./image/9f1d99d6-bf62-417e-be99-2ac49782bf19.png)


> C++优化版本的运行效率：
>
> ![image](./image/5a54e4bb-3106-4564-b547-6b10feb9efe1.png)
>
> ![image](./image/04d21912-06f4-42f9-99b8-f1badeb86e1c.png)
>
> ![image](./image/5d6a3e1f-4954-4d1f-8504-a493d694c39b.png)
>
> ![image](./image/593580ec-7d79-42e4-a857-2bb8d5c6f974.png)
>
> ![image](./image/2683225e-59d1-4731-b563-8d6cd3b1ca48.png)

> linux下优化版本的运行效率：
>
> ![2c58550d935bb7079db5ea3342282fdc](./image/b8d2060d-b8ea-4ced-a045-7dea13d106e8.png)

- 效率对比表：

|             | 1    | 2    | 3    | 4    | 5    | 平均时间 |
| ----------- | ---- | ---- | ---- | ---- | ---- | -------- |
| gmssl版本   | 0.007920 | 0.008905 | 0.008681 | 0.008312 | 0.008035 | 0.008371 |
| python版本  | 0.003987 | 0.004088 | 0.004861 | 0.005983 | 0.005999 | 0.004984 |
| C++基础版本 | 0.001516 | 0.001937 | 0.001897 | 0.001570 | 0.001565 | 0.001697 |
| C++优化版本 | 0.001247 | 0.001232 | 0.001268 | 0.001419 | 0.001239 | 0.001281 |
| Linux优化版本 | 16微秒 | 20微秒 | 19微秒 | 29微秒 | 27微秒 | 22.2微秒 |

- 效率对比图：将Linux优化版本的单位统一成秒。

![image](./image/45ec5953-f88e-4fb6-bfae-076e2ec2aa54.png)

gmssl版本到python版本以及python版本到C++版本效率提升较为明显，C++版本在进行优化后略有提升，最终优化了近7倍。再加上Linux下的优化（非常明显），最终优化了377倍:astonished:。
