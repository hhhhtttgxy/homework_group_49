# AES impl with ARM instruction
# 使用ARM指令实现AES

|     代码名称      |                    具体实现                     |
| :---------------: | :---------------------------------------------: |
|   project_8.py    |   PPT中使用ARM指令对AES的实现（参考文献[1]）    |
|    AES_ARM64.s    | 开源代码中使用ARM汇编对AES的实现（参考文献[3]） |
| AES_ARM（文件夹） | 开源代码中使用ARM指令对AES的实现（参考文献[4]） |

## 1. 实现原理

NEON就是一种基于SIMD思想的ARM技术，相比于ARMv6或之前的架构，NEON结合了64-bit和128-bit的SIMD指令集，提供128-bit宽的向量运算(vector operations)。NEON技术从ARMv7开始被采用，目前可以在ARM Cortex-A和Cortex-R系列处理器中采用。NEON在Cortex-A7、Cortex-A12、Cortex-A15处理器中被设置为默认选项，但是在其余的ARMv7 Cortex-A系列中是可选项。NEON与VFP共享了同样的寄存器，但它具有自己独立的执行流水线。

## 2. 实现过程

- aes128_enc_armv8 函数：该函数用于执行 AES-128 的加密算法，输入参数为一个 16 字节的明文块 in，一个用于存储密文的数组 ou 和经过密钥扩展的轮密钥数组 rk。该函数使用 NEON 指令加载明文块和轮密钥的初始值，并重复 9 轮的过 S 盒、行移位、列混合、轮密钥加，第 10 轮没有列混合。最后，将计算得到的密文块存储到 ou 中。
```C++
void aes128_enc_armv8(const uint8_t in[16], uint8_t ou[16], const uint32_t rk[44])
{
    uint8x16_t block = vld1q_u8(in);
    uint8_t* p8 = (uint8_t*)rk;
    block = vaesmcq_u8(vaeseq_u8(block, vld1q_u8(p8 + 16 * 0)));
    block = vaesmcq_u8(vaeseq_u8(block, vld1q_u8(p8 + 16 * 1)));
    block = vaesmcq_u8(vaeseq_u8(block, vld1q_u8(p8 + 16 * 2)));
    block = vaesmcq_u8(vaeseq_u8(block, vld1q_u8(p8 + 16 * 3)));
    block = vaesmcq_u8(vaeseq_u8(block, vld1q_u8(p8 + 16 * 4)));
    block = vaesmcq_u8(vaeseq_u8(block, vld1q_u8(p8 + 16 * 5)));
    block = vaesmcq_u8(vaeseq_u8(block, vld1q_u8(p8 + 16 * 6)));
    block = vaesmcq_u8(vaeseq_u8(block, vld1q_u8(p8 + 16 * 7)));
    block = vaesmcq_u8(vaeseq_u8(block, vld1q_u8(p8 + 16 * 8)));
    block = vaeseq_u8(block, vld1q_u8(p8 + 16 * 9));
    block = veorq_u8(block, vld1q_u8(p8 + 16 * 10));

    vst1q_u8(ou, block);
}
```
- 类似的可以实现解密算法。
```C++
void aes128_dec_armv8(const uint8_t in[16], uint8_t ou[16], const uint32_t rk[44])
{
    uint8x16_t block = vld1q_u8(in);
    uint8_t* p8 = (uint8_t*)rk;
    block = vaesimcq_u8(vaesdq_u8(block, vld1q_u8(p8 + 16 * 0)));
    block = vaesimcq_u8(vaesdq_u8(block, vld1q_u8(p8 + 16 * 1)));
    block = vaesimcq_u8(vaesdq_u8(block, vld1q_u8(p8 + 16 * 2)));
    block = vaesimcq_u8(vaesdq_u8(block, vld1q_u8(p8 + 16 * 3)));
    block = vaesimcq_u8(vaesdq_u8(block, vld1q_u8(p8 + 16 * 4)));
    block = vaesimcq_u8(vaesdq_u8(block, vld1q_u8(p8 + 16 * 5)));
    block = vaesimcq_u8(vaesdq_u8(block, vld1q_u8(p8 + 16 * 6)));
    block = vaesimcq_u8(vaesdq_u8(block, vld1q_u8(p8 + 16 * 7)));
    block = vaesimcq_u8(vaesdq_u8(block, vld1q_u8(p8 + 16 * 8)));
    block = vaesdq_u8(block, vld1q_u8(p8 + 16 * 9));
    block = veorq_u8(block, vld1q_u8(p8 + 16 * 10));

    vst1q_u8(ou, block);
}
```
- main 函数：首先定义明文块和密钥以及扩展后的轮密钥，然后还有一个数组用于存储加密后的密文，然后调用 aes128_enc_armv8 函数对明文进行加密，得到密文。最后，输出明文和密文。
```C++
int main()
{
    uint8_t key[16];
    uint32_t round_keys[44];
    uint8_t plaintext[16];
    uint8_t ciphertext[16];

    aes128_enc_armv8(plaintext, ciphertext, round_keys);

    cout << "明文：";
    for (int i = 0; i < 16; i++)
        cout << hex << plaintext[i] << " ";
    cout << endl;

    cout << "密文：";
    for (int i = 0; i < 16; i++)
        cout << hex << ciphertext[i] << " ";
    cout << endl;

    return 0;
}
```
> 注：由于设备原因无法进行ARM编译，因此代码并未经过验证。


## 3. 补充

经查询相关资料，后续补充了开源代码中ARM汇编对AES的实现以及一个ARM指令对AES的实现的文件夹，主要介绍文件夹中的实现，已经将介绍放在该文件夹内，然后在参考文献中又补充了三个仓库均涉及相关实现（参考文献[5][6][7]）。


## 4. 参考文献
[1] 20230331-sm4-public.pdf

[2] https://tinycrypt.wordpress.com/2018/03/16/aes-tiny/

[3] https://github.com/odzhan/aes_dust/tree/master/asm/arm64

[4] https://github.com/mike76-dev/aes-arm64

[5] https://github.com/junwei-wang/AES-ARM-NEON

[6] https://github.com/ReinForce-II/tiny_arm_aes_lib

[7] https://github.com/jkivilin/camellia-simd-aesni/tree/master

[8] https://docs.unity3d.com/Packages/com.unity.burst@1.6/api/Unity.Burst.Intrinsics.Arm.Neon.html

> 注：参考文献[8]是ARM中NEON相关的使用方法，非常具体，也就不再展示了。
