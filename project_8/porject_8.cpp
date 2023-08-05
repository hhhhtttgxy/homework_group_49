#include <iostream>
#include <arm_neon.h>
using namespace std;

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
