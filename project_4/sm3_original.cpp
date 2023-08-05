#include <iostream>
#include <iomanip>
#include <windows.h>

#define MOD 4294967296 //2^32
using namespace std;

const unsigned int IV[8] = { 0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e };//初始iv

unsigned int T(int j)
{
    if (j >= 0 && j <= 15)
        return 0x79cc4519; //32
    else
        return 0x7a879d8a;
}

unsigned int FF(int j, unsigned int X, unsigned int Y, unsigned int Z)
{
    unsigned int result;
    if (j >= 0 && j <= 15)
    {
        result = X ^ Y ^ Z;
        return result; //32
    }
    else
    {
        result = (X & Y) | (X & Z) | (Y & Z);
        return result;
    }
}

unsigned int GG(int j, unsigned int X, unsigned int Y, unsigned int Z)
{
    unsigned int result;
    if (j >= 0 && j <= 15)
    {
        result = X ^ Y ^ Z;
        return result; //32
    }
    else
    {
        unsigned int X_f = X ^ 0xffffffff;
        result = (X & Y) | (X_f & Z);
        return result;
    }
}

unsigned int shift_left(unsigned int X, int n)
{
    if (n > 32)
        n = n - 32;
    unsigned int result = ((X << n) | (X >> (32 - n))) & 0xffffffff;
    return result; //32
}

unsigned int P0(unsigned int X)
{
    unsigned int result = X ^ shift_left(X, 9) ^ shift_left(X, 17);
    result = result & 0xffffffff;
    return result;
}


unsigned int P1(unsigned int X)
{
    unsigned int result = X ^ shift_left(X, 15) ^ shift_left(X, 23);
    result = result & 0xffffffff;
    return result;
}

void CF(unsigned int* V, unsigned int* Bi, int n)
{
    unsigned int W[68] = { 0 };
    unsigned int W_[64] = { 0 };
    for (int i = 0; i < 16; i++)
        W[i] = (Bi[16 * n + i]) & 0xffffffff;
    for (int j = 16; j < 68; j++)
    {
        int X = W[j - 16] ^ W[j - 9] ^ shift_left(W[j - 3], 15);
        W[j] = P1(X) ^ shift_left(W[j - 13], 7) ^ W[j - 6];
    }
    for (int j = 0; j < 64; j++)
        W_[j] = W[j] ^ W[j + 4];
    /*
    for (int j = 0; j < 68; j++)
    {
        cout << setfill('0') << hex << setw(8) << W[j] << " ";
    }
    cout << endl;
    cout << endl;
    for (int j = 0; j < 64; j++)
    {
        cout << setfill('0') << hex << setw(8) << W_[j] << " ";
    }
    cout << endl;
    cout << endl;
    */
    unsigned int A = V[n * 8];
    unsigned int B = V[n * 8 + 1];
    unsigned int C = V[n * 8 + 2];
    unsigned int D = V[n * 8 + 3];
    unsigned int E = V[n * 8 + 4];
    unsigned int F = V[n * 8 + 5];
    unsigned int G = V[n * 8 + 6];
    unsigned int H = V[n * 8 + 7];
    unsigned int SS1;
    unsigned int SS2;
    unsigned int TT1;
    unsigned int TT2;

    //cout << "   " << setfill('0') << hex << setw(8) << A << " " << setw(8) << B << " " << setw(8) << C << " " << setw(8) << D << " " << setw(8) << E << " " << setw(8) << F << " " << setw(8) << G << " " << setw(8) << H << endl;

    for (int j = 0; j < 64; j++)
    {
        SS1 = shift_left((shift_left(A, 12) + E + shift_left(T(j), j)) % MOD, 7);
        SS2 = SS1 ^ shift_left(A, 12);
        TT1 = (FF(j, A, B, C) + D + SS2 + W_[j]) % MOD;
        TT2 = (GG(j, E, F, G) + H + SS1 + W[j]) % MOD;
        D = C;
        C = shift_left(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = shift_left(F, 19);
        F = E;
        E = P0(TT2);
        //cout << setfill(' ') << dec << setw(2) << j << " " << setfill('0') << hex << setw(8) << A << " "<< setw(8) << B << " " << setw(8) << C << " " << setw(8) << D << " "<< setw(8) << E << " " << setw(8) << F << " " << setw(8) << G << " " << setw(8) << H <<endl;
    }
    //cout << endl;
    V[(n + 1) * 8] = A ^ V[n * 8];
    V[(n + 1) * 8 + 1] = B ^ V[n * 8 + 1];
    V[(n + 1) * 8 + 2] = C ^ V[n * 8 + 2];
    V[(n + 1) * 8 + 3] = D ^ V[n * 8 + 3];
    V[(n + 1) * 8 + 4] = E ^ V[n * 8 + 4];
    V[(n + 1) * 8 + 5] = F ^ V[n * 8 + 5];
    V[(n + 1) * 8 + 6] = G ^ V[n * 8 + 6];
    V[(n + 1) * 8 + 7] = H ^ V[n * 8 + 7];
}

void sm3(const int message[], int len_byte)
{
    int len_bit = 8 * len_byte;
    int k = (448 - 1 - len_bit) % 512;
    if (k < 0)
        k += 512;
    int len_f = len_bit + k + 65;
    int len_fB = len_f / 8;
    unsigned int* F = new unsigned int[len_fB];

    for (int i = 0; i < len_fB; i++)
    {
        if (i < len_byte)
            F[i] = message[i];
        else if (i == len_byte)
            F[i] = 0x80;
        else
            F[i] = 0x00;
    }

    unsigned long long bit_length = (len_bit);
    F[len_fB - 1] = (bit_length & 0xff);
    F[len_fB - 2] = ((bit_length >> 8) & 0xff);
    F[len_fB - 3] = ((bit_length >> 16) & 0xff);
    F[len_fB - 4] = ((bit_length >> 24) & 0xff);
    F[len_fB - 5] = ((bit_length >> 32) & 0xff);
    F[len_fB - 6] = ((bit_length >> 40) & 0xff);
    F[len_fB - 7] = ((bit_length >> 48) & 0xff);
    F[len_fB - 8] = ((bit_length >> 56) & 0xff);

    unsigned int* B = new unsigned int[len_fB / 4];
    unsigned int* V = new unsigned int[(len_f / 64) + 8];

    for (int i = 0; i < len_fB / 4; i++)
        B[i] = ((F[i * 4] << 24) | (F[i * 4 + 1] << 16) | (F[i * 4 + 2] << 8) | F[i * 4 + 3]) & 0xffffffff;
    for (int i = 0; i < 8; i++)
        V[i] = IV[i];
    for (int i = 0; i < len_f / 512; i++)
        CF(V, B, i);
    for (int i = 0; i < 8; i++)
        cout << hex << V[len_f / 64 + i] << " ";
    cout << endl;

    delete[] F;
    delete[] B;
    delete[] V;
}

int main()
{
    const int message[] = { 0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,
                        0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,
                        0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,
                        0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64,0x61,0x62,0x63,0x64 };
    LARGE_INTEGER BegainTime;
    LARGE_INTEGER EndTime;
    LARGE_INTEGER Frequency;
    QueryPerformanceFrequency(&Frequency);
    QueryPerformanceCounter(&BegainTime);
    int len_byte = sizeof(message) / sizeof(message[0]);
    sm3(message, len_byte);
    QueryPerformanceCounter(&EndTime);
    cout << "用时：" << (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart << "秒" << endl;
    return 0;
}
