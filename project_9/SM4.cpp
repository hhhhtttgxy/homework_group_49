#include<iostream>
#include <iomanip>
#include"windows.h"
using namespace std;

const unsigned int S_box[16][16] = { 0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,0x05,
                                     0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,0x06,0x99,
                                     0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,0xcf,0xac,0x62,
                                     0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,0x75,0x8f,0x3f,0xa6,
                                     0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,0x19,0xe6,0x85,0x4f,0xa8,
                                     0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,0x0f,0x4b,0x70,0x56,0x9d,0x35,
                                     0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,0x22,0x7c,0x3b,0x01,0x21,0x78,0x87,
                                     0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e,
                                     0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1,
                                     0xe0,0xae,0x5d,0xa4,0x9b,0x34,0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3,
                                     0x1d,0xf6,0xe2,0x2e,0x82,0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f,
                                     0xd5,0xdb,0x37,0x45,0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51,
                                     0x8d,0x1b,0xaf,0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8,
                                     0x0a,0xc1,0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0,
                                     0x89,0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84,
                                     0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,0x48 };

const unsigned int FK[4] = { 0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC };

const unsigned int CK[32] = { 0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
                              0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
                              0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
                              0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
                              0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
                              0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
                              0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
                              0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279 };

unsigned int S_Byte(unsigned int byte) //字节过S盒
{
    int h, l;
    h = byte >> 4;
    l = byte & 15;
    byte = S_box[h][l];
    return byte;
}

unsigned int shift_left(unsigned int X, int n)
{
    unsigned int result = ((X << n) | (X >> (32 - n))) & 0xffffffff;
    return result; 
}

unsigned int T(unsigned int A) //合成置换
{
    unsigned int a[4];
    a[0] = (A >> 24) & 0xff;
    a[1] = (A >> 16) & 0xff;
    a[2] = (A >> 8) & 0xff;
    a[3] = A & 0xff;
    for (int i = 0; i < 4; i++)
    {
        a[i] = S_Byte(a[i]); //非线性变换
    }
    unsigned int B = (a[0] << 24) | (a[1] << 16) | (a[2] << 8) | a[3];
    B = B ^ shift_left(B, 2) ^ shift_left(B, 10) ^ shift_left(B, 18) ^ shift_left(B, 24); //线性变换
    return B;
} 

unsigned int T_(unsigned int A)
{
    unsigned char a[4];
    a[0] = (A >> 24) & 0xff;
    a[1] = (A >> 16) & 0xff;
    a[2] = (A >> 8) & 0xff;
    a[3] = A & 0xff;
    for (int i = 0; i < 4; i++)
    {
        a[i] = S_Byte(a[i]); //非线性变换
    }
    unsigned int B = (a[0] << 24) | (a[1] << 16) | (a[2] << 8) | a[3];
    B = B ^ shift_left(B, 13) ^ shift_left(B, 23); //线性变换
    return B;
}

void KeyExpansion(unsigned int MK[4], unsigned int rk[32]) //密钥扩展
{
    unsigned int K[36];
    for (int i = 0; i < 4; i++)
    {
        K[i] = MK[i] ^ FK[i];
    }
    for (int i = 0; i < 32; i++)
    {
        rk[i] = K[i + 4] = K[i] ^ T_(K[i + 1] ^ K[i + 2] ^ K[i + 3] ^ CK[i]);
    }
}

void SM4_Encrypt(unsigned int Plain[4], unsigned int Cipher[4], unsigned int rk[32])
{
    unsigned int X[36];
    for (int i = 0; i < 4; i++)
    {
        X[i] = Plain[i];
    }
    for (int i = 0; i < 32; i++)
    {
        X[i + 4] = X[i] ^ T(X[i + 1] ^ X[i + 2] ^ X[i + 3] ^ rk[i]); //F函数
    }
    for (int i = 0; i < 4; i++)
    {
        Cipher[i] = X[35 - i];
    }
    /*
    cout << "每轮输出状态：" << endl;
    for (int i = 0; i < 32; i++)
    {
        cout << hex << setw(8) << setfill('0') << X[i+4] << endl;
    }
    cout << endl;
    */
}

void SM4_Decrypt(unsigned int Plain[4], unsigned int Cipher[4], unsigned int rk[32])
{
    unsigned int X[36];
    for (int i = 0; i < 4; i++)
    {
        X[i] = Cipher[i];
    }
    for (int i = 0; i < 32; i++)
    {
        X[i + 4] = X[i] ^ T(X[i + 1] ^ X[i + 2] ^ X[i + 3] ^ rk[31 - i]); //F函数
    }
    for (int i = 0; i < 4; i++)
    {
        Plain[i] = X[35 - i];
    }
}

int main()
{
    unsigned int Plain[4] = { 0x01234567,0x89abcdef,0xfedcba98,0x76543210 };
    unsigned int Key[32] = { 0x01234567,0x89abcdef,0xfedcba98,0x76543210 }; 
    unsigned int Cipher[4]; 
    unsigned int rk[32]; 
    cout << "明文：" << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << hex << setw(8) << setfill('0') << Plain[i];
    }
    cout << endl;
    cout << endl;
    LARGE_INTEGER BegainTime;
    LARGE_INTEGER EndTime;
    LARGE_INTEGER Frequency;
    QueryPerformanceFrequency(&Frequency);
    QueryPerformanceCounter(&BegainTime);
    KeyExpansion(Key, rk);
    QueryPerformanceCounter(&EndTime);
    cout << "密钥扩展用时：" << (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart << "秒" << endl;
    /*
    cout << "轮密钥：" << endl;
    for (int i = 0; i < 32; i++)
    {
        cout << hex << setw(8) << setfill('0') << rk[i] << endl;
    }
    cout << endl;
    */
    LARGE_INTEGER BegainTime1;
    LARGE_INTEGER EndTime1;
    LARGE_INTEGER Frequency1;
    QueryPerformanceFrequency(&Frequency1);
    QueryPerformanceCounter(&BegainTime1);
    SM4_Encrypt(Plain, Cipher, rk);  //加密
    QueryPerformanceCounter(&EndTime1);
    cout << "加密用时：" << (double)(EndTime1.QuadPart - BegainTime1.QuadPart) / Frequency1.QuadPart << "秒" << endl;
    cout << "密文：" << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << hex << setw(8) << setfill('0') << Cipher[i];
    }
    cout << endl;
    cout << endl;
    unsigned int Plain_[4]; //解密后的明文
    LARGE_INTEGER BegainTime2;
    LARGE_INTEGER EndTime2;
    LARGE_INTEGER Frequency2;
    QueryPerformanceFrequency(&Frequency2);
    QueryPerformanceCounter(&BegainTime2);
    SM4_Decrypt(Plain_, Cipher, rk);  //解密
    QueryPerformanceCounter(&EndTime2);
    cout << "解密用时：" << (double)(EndTime2.QuadPart - BegainTime2.QuadPart) / Frequency2.QuadPart << "秒" << endl;
    cout << "解密后的明文：" << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << hex << setw(8) << setfill('0') << Plain_[i];
    }
    cout << endl;
    cout << endl;
    LARGE_INTEGER BegainTime3;
    LARGE_INTEGER EndTime3;
    LARGE_INTEGER Frequency3;
    QueryPerformanceFrequency(&Frequency3);
    QueryPerformanceCounter(&BegainTime3);
    for (int i = 0; i < 1000000; i++)
    {
        SM4_Encrypt(Plain, Plain, rk);
    }
    QueryPerformanceCounter(&EndTime3);
    cout << "加密1000000次用时：" << (double)(EndTime3.QuadPart - BegainTime3.QuadPart) / Frequency3.QuadPart << "秒" << endl;
    cout << "加密1000000次的密文：" << endl;
    for (int i = 0; i < 4; i++)
    {
        cout << hex << setw(8) << setfill('0') << Plain[i];
    }
    return 0;
}
