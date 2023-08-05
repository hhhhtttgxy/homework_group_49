/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   aes_bitslice.cpp
 * Author: mike76
 *
 * Created on 27 June 2020, 12:26
 */

#include <stdio.h>
#include "arm_neon.h"
#include <stdlib.h>
#include <time.h>

void print_vector(uint8x16_t v)
{
	uint8_t c[16];
	vst1q_u8(c, v);
	for (uint8_t i = 0; i < 16; i++) printf("%02x", (unsigned char)c[i]);
}

static const uint8x16_t M0 = {
	0x00, 0x04, 0x08, 0x0c, 0x01, 0x05, 0x09, 0x0d,
	0x02, 0x06, 0x0a, 0x0e, 0x03, 0x07, 0x0b, 0x0f
};

static const uint8x16_t SR = {
	0x00, 0x01, 0x02, 0x03, 0x05, 0x06, 0x07, 0x04,
	0x0a, 0x0b, 0x08, 0x09, 0x0f, 0x0c, 0x0d, 0x0e
};

static const uint8x16_t R32D = {
	0x07, 0x07, 0x07, 0x07, 0x0b, 0x0b, 0x0b, 0x0b,
	0x0f, 0x0f, 0x0f, 0x0f, 0x03, 0x03, 0x03, 0x03
};

static const uint8x16_t NR32D = {
	0x03, 0x03, 0x03, 0x03, 0x07, 0x07, 0x07, 0x07,
	0x0b, 0x0b, 0x0b, 0x0b, 0x0f, 0x0f, 0x0f, 0x0f
};

static const uint8x16_t RCON = {
	0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

static inline void swapmove_2x(uint8x16_t *a0, uint8x16_t *b0, uint8x16_t *a1,
	uint8x16_t *b1, uint8x16_t mask, int n)
{
	uint8x16_t t0, t1;
	t0 = (uint8x16_t)vshrq_n_u64(vreinterpretq_u64_u8(*b0), n);
	t1 = (uint8x16_t)vshrq_n_u64(vreinterpretq_u64_u8(*b1), n);
	t0 = veorq_u8(t0, *a0);
	t1 = veorq_u8(t1, *a1);
	t0 = vandq_u8(t0, mask);
	t1 = vandq_u8(t1, mask);
	*a0 = veorq_u8(*a0, t0);
	t0 = (uint8x16_t)vshlq_n_u64(vreinterpretq_u64_u8(t0), n);
	*a1 = veorq_u8(*a1, t1);
	t1 = (uint8x16_t)vshlq_n_u64(vreinterpretq_u64_u8(t1), n);
	*b0 = veorq_u8(*b0, t0);
	*b1 = veorq_u8(*b1, t1);
}

static inline void bitslice(uint8x16_t *x7, uint8x16_t *x6,
	uint8x16_t *x5, uint8x16_t *x4, uint8x16_t *x3,
	uint8x16_t *x2, uint8x16_t *x1, uint8x16_t *x0)
{
	uint8x16_t t0, t1;
	t0 = vdupq_n_u8(0x55);
	t1 = vdupq_n_u8(0x33);
	swapmove_2x(x0, x1, x2, x3, t0, 1);
	swapmove_2x(x4, x5, x6, x7, t0, 1);
	t0 = vdupq_n_u8(0x0f);
	swapmove_2x(x0, x2, x1, x3, t1, 2);
	swapmove_2x(x4, x6, x5, x7, t1, 2);
	swapmove_2x(x0, x4, x1, x5, t0, 4);
	swapmove_2x(x2, x6, x3, x7, t0, 4);
	*x0 = vqtbl1q_u8(*x0, M0);
	*x1 = vqtbl1q_u8(*x1, M0);
	*x2 = vqtbl1q_u8(*x2, M0);
	*x3 = vqtbl1q_u8(*x3, M0);
	*x4 = vqtbl1q_u8(*x4, M0);
	*x5 = vqtbl1q_u8(*x5, M0);
	*x6 = vqtbl1q_u8(*x6, M0);
	*x7 = vqtbl1q_u8(*x7, M0);
}

#define IN_BS_CH(b0, b1, b2, b3, b4, b5, b6, b7) \
	b2 = veorq_u8(b2, b1); \
	b5 = veorq_u8(b5, b6); \
	b3 = veorq_u8(b3, b0); \
	b6 = veorq_u8(b6, b2); \
	b5 = veorq_u8(b5, b0); \
	b6 = veorq_u8(b6, b3); \
	b3 = veorq_u8(b3, b7); \
	b7 = veorq_u8(b7, b5); \
	b3 = veorq_u8(b3, b4); \
	b4 = veorq_u8(b4, b5); \
	b2 = veorq_u8(b2, b7); \
	b3 = veorq_u8(b3, b1); \
	b1 = veorq_u8(b1, b5)

#define OUT_BS_CH(b0, b1, b2, b3, b4, b5, b6, b7, t0, t1) \
	t0 = veorq_u8(b0, b6); \
	b0 = veorq_u8(b5, b3); \
	t1 = veorq_u8(b4, b6); \
	b6 = veorq_u8(b1, t1); \
	b1 = veorq_u8(b1, b4); \
	b1 = veorq_u8(b1, b5); \
	b4 = veorq_u8(b3, b7); \
	b3 = veorq_u8(b2, t0); \
	b3 = veorq_u8(b3, b0); \
	b2 = veorq_u8(b7, b0); \
	b7 = veorq_u8(b4, t1); \
	b7 = veorq_u8(b7, b5); \
	b5 = t0

#define MUL_GF4(x0, x1, y0, y1, t0, t1) \
	t0 = veorq_u8(y0, y1); \
	t0 = vandq_u8(t0, x0); \
	x0 = veorq_u8(x0, x1); \
	t1 = vandq_u8(x1, y0); \
	x0 = vandq_u8(x0, y1); \
	x1 = veorq_u8(t1, t0); \
	x0 = veorq_u8(x0, t1)

#define MUL_GF4_N_GF4(x0, x1, y0, y1, t0, x2, x3, y2, y3, t1) \
	t0 = veorq_u8(y0, y1); \
	t1 = veorq_u8(y2, y3); \
	t0 = vandq_u8(t0, x0); \
	t1 = vandq_u8(t1, x2); \
	x0 = veorq_u8(x0, x1); \
	x2 = veorq_u8(x2, x3); \
	x1 = vandq_u8(x1, y0); \
	x3 = vandq_u8(x3, y2); \
	x0 = vandq_u8(x0, y1); \
	x2 = vandq_u8(x2, y3); \
	x1 = veorq_u8(x1, x0); \
	x2 = veorq_u8(x2, x3); \
	x0 = veorq_u8(x0, t0); \
	x3 = veorq_u8(x3, t1)

#define MUL_GF16_2(x0, x1, x2, x3, x4, x5, x6, x7, \
	y0, y1, y2, y3, t0, t1, t2, t3) \
	t0 = veorq_u8(x0, x2); \
	t1 = veorq_u8(x1, x3); \
	MUL_GF4(x0, x1, y0, y1, t2, t3); \
	y0 = veorq_u8(y0, y2); \
	y1 = veorq_u8(y1, y3); \
	MUL_GF4_N_GF4(t0, t1, y0, y1, t3, x2, x3, y2, y3, t2); \
	x0 = veorq_u8(x0, t0); \
	x2 = veorq_u8(x2, t0); \
	x1 = veorq_u8(x1, t1); \
	x3 = veorq_u8(x3, t1); \
	t0 = veorq_u8(x4, x6); \
	t1 = veorq_u8(x5, x7); \
	MUL_GF4_N_GF4(t0, t1, y0, y1, t3, x6, x7, y2, y3, t2); \
	y0 = veorq_u8(y0, y2); \
	y1 = veorq_u8(y1, y3); \
	MUL_GF4(x4, x5, y0, y1, t2, t3); \
	x4 = veorq_u8(x4, t0); \
	x6 = veorq_u8(x6, t0); \
	x5 = veorq_u8(x5, t1); \
	x7 = veorq_u8(x7, t1)

#define INV_GF256(x0, x1, x2, x3, x4, x5, x6, x7, \
	t0, t1, t2, t3, s0, s1, s2, s3) \
	t3 = veorq_u8(x4, x6); \
	t0 = veorq_u8(x5, x7); \
	t1 = veorq_u8(x1, x3); \
	s1 = veorq_u8(x7, x6); \
	s0 = veorq_u8(x0, x2); \
	s3 = veorq_u8(t3, t0); \
	t2 = vorrq_u8(t0, t1); \
	s2 = vandq_u8(t3, s0); \
	t3 = vorrq_u8(t3, s0); \
	s0 = veorq_u8(s0, t1); \
	t0 = vandq_u8(t0, t1); \
	t1 = veorq_u8(x3, x2); \
	s3 = vandq_u8(s3, s0); \
	s1 = vandq_u8(s1, t1); \
	t1 = veorq_u8(x4, x5); \
	s0 = veorq_u8(x1, x0); \
	t3 = veorq_u8(t3, s1); \
	t2 = veorq_u8(t2, s1); \
	s1 = vandq_u8(t1, s0); \
	t1 = vorrq_u8(t1, s0); \
	t3 = veorq_u8(t3, s3); \
	t0 = veorq_u8(t0, s1); \
	t2 = veorq_u8(t2, s2); \
	t1 = veorq_u8(t1, s3); \
	t0 = veorq_u8(t0, s2); \
	s0 = vandq_u8(x7, x3); \
	t1 = veorq_u8(t1, s2); \
	s1 = vandq_u8(x6, x2); \
	s2 = vandq_u8(x5, x1); \
	s3 = vorrq_u8(x4, x0); \
	t3 = veorq_u8(t3, s0); \
	t1 = veorq_u8(t1, s2); \
	s0 = veorq_u8(t0, s3); \
	t2 = veorq_u8(t2, s1); \
	s2 = vandq_u8(t3, t1); \
	s1 = veorq_u8(t2, s2); \
	s3 = veorq_u8(s0, s2); \
	s1 = vbslq_u8(s1, t1, s0); \
	t0 = vmvnq_u8(s0); \
	s0 = vbslq_u8(s0, s1, s3); \
	t0 = vbslq_u8(t0, s1, s3); \
	s3 = vbslq_u8(s3, t3, t2); \
	t3 = veorq_u8(t3, t2); \
	s2 = vandq_u8(s0, s3); \
	t1 = veorq_u8(t1, t0); \
	s2 = veorq_u8(s2, t3); \
	MUL_GF16_2(x0, x1, x2, x3, x4, x5, x6, x7, \
		s3, s2, s1, t1, s0, t0, t2, t3)

#define SBOX(b0, b1, b2, b3, b4, b5, b6, b7, \
	t0, t1, t2, t3, s0, s1, s2, s3) \
	IN_BS_CH(b0, b1, b2, b3, b4, b5, b6, b7); \
	INV_GF256(b6, b5, b0, b3, b7, b1, b4, b2, \
		t0, t1, t2, t3, s0, s1, s2, s3); \
	OUT_BS_CH(b7, b1, b4, b2, b6, b5, b0, b3, t0, t1); \
	b0 = vmvnq_u8(b0); \
	b1 = vmvnq_u8(b1); \
	b5 = vmvnq_u8(b5); \
	b6 = vmvnq_u8(b6)

#define MIX_COLS(x0, x1, x2, x3, x4, x5, x6, x7, \
	t0, t1, t2, t3, t4, t5, t6, t7) \
	t0 = vextq_u8(x0, x0, 4); \
	t1 = vextq_u8(x1, x1, 4); \
	t2 = vextq_u8(x2, x2, 4); \
	t3 = vextq_u8(x3, x3, 4); \
	t4 = vextq_u8(x4, x4, 4); \
	t5 = vextq_u8(x5, x5, 4); \
	t6 = vextq_u8(x6, x6, 4); \
	t7 = vextq_u8(x7, x7, 4); \
	x0 = veorq_u8(x0, t0); \
	x1 = veorq_u8(x1, t1); \
	x2 = veorq_u8(x2, t2); \
	x3 = veorq_u8(x3, t3); \
	x4 = veorq_u8(x4, t4); \
	x5 = veorq_u8(x5, t5); \
	x6 = veorq_u8(x6, t6); \
	x7 = veorq_u8(x7, t7); \
	t1 = veorq_u8(t1, x0); \
	t2 = veorq_u8(t2, x1); \
	t3 = veorq_u8(t3, x2); \
	t4 = veorq_u8(t4, x3); \
	t5 = veorq_u8(t5, x4); \
	t6 = veorq_u8(t6, x5); \
	t7 = veorq_u8(t7, x6); \
	x0 = vextq_u8(x0, x0, 8); \
	x1 = vextq_u8(x1, x1, 8); \
	x2 = vextq_u8(x2, x2, 8); \
	x3 = vextq_u8(x3, x3, 8); \
	x4 = vextq_u8(x4, x4, 8); \
	x5 = vextq_u8(x5, x5, 8); \
	x6 = vextq_u8(x6, x6, 8); \
	t0 = veorq_u8(t0, x7); \
	t1 = veorq_u8(t1, x7); \
	t3 = veorq_u8(t3, x7); \
	t4 = veorq_u8(t4, x7); \
	x7 = vextq_u8(x7, x7, 8); \
	x0 = veorq_u8(x0, t0); \
	x1 = veorq_u8(x1, t1); \
	x2 = veorq_u8(x2, t2); \
	x3 = veorq_u8(x3, t3); \
	x4 = veorq_u8(x4, t4); \
	x5 = veorq_u8(x5, t5); \
	x6 = veorq_u8(x6, t6); \
	x7 = veorq_u8(x7, t7)

#define SHIFT_ROWS(x0, x1, x2, x3, x4, x5, x6, x7, mask) \
	x0 = vqtbl1q_u8(x0, mask); \
	x1 = vqtbl1q_u8(x1, mask); \
	x2 = vqtbl1q_u8(x2, mask); \
	x3 = vqtbl1q_u8(x3, mask); \
	x4 = vqtbl1q_u8(x4, mask); \
	x5 = vqtbl1q_u8(x5, mask); \
	x6 = vqtbl1q_u8(x6, mask); \
	x7 = vqtbl1q_u8(x7, mask)

static inline uint8x16_t sl_xor(uint8x16_t tmp1)
{
	uint8x16_t tmp4;
	tmp4 = (uint8x16_t)vshlq_n_u32(vreinterpretq_u32_u8(tmp1), 8);
	tmp1 = veorq_u8(tmp1, tmp4);
	tmp4 = (uint8x16_t)vshlq_n_u32(vreinterpretq_u32_u8(tmp1), 8);
	tmp1 = veorq_u8(tmp1, tmp4);
	tmp4 = (uint8x16_t)vshlq_n_u32(vreinterpretq_u32_u8(tmp1), 8);
	tmp1 = veorq_u8(tmp1, tmp4);
	return tmp1;
}

uint8_t gen_keys(const uint8_t *input_key, uint8x16_t *keys, const uint16_t keylen)
{

	uint8_t i, numkeys;
	uint32_t rcon;
	uint8x16_t temp;
	uint8x16_t m1, m2, m4, m8, m10, m20, m40, m80;
	uint8x16_t t0, t1, t2, t3, t4, t5, t6, t7;
	uint8x16_t s0, s1, s2, s3, s4, s5, s6, s7;

	m1 = vdupq_n_u8(0x01);
	m2 = vdupq_n_u8(0x02);
	m4 = vdupq_n_u8(0x04);
	m8 = vdupq_n_u8(0x08);
	m10 = vdupq_n_u8(0x10);
	m20 = vdupq_n_u8(0x20);
	m40 = vdupq_n_u8(0x40);
	m80 = vdupq_n_u8(0x80);

	switch(keylen) {

	case 128:
		numkeys = 88;
		temp = vld1q_u8(input_key);
		temp = vqtbl1q_u8(temp, M0);
		t0 = vtstq_u8(temp, m1);
		t1 = vtstq_u8(temp, m2);
		t2 = vtstq_u8(temp, m4);
		t3 = vtstq_u8(temp, m8);
		t4 = vtstq_u8(temp, m10);
		t5 = vtstq_u8(temp, m20);
		t6 = vtstq_u8(temp, m40);
		t7 = vtstq_u8(temp, m80);
		*keys = t0;
		*(keys + 1) = t1;
		*(keys + 2) = t2;
		*(keys + 3) = t3;
		*(keys + 4) = t4;
		*(keys + 5) = t5;
		*(keys + 6) = t6;
		*(keys + 7) = t7;
		keys += 8;
		rcon = 0x01;
		for (i = 0; i < 10; i++) {
			*keys = sl_xor(t0);
			*(keys + 1) = sl_xor(t1);
			*(keys + 2) = sl_xor(t2);
			*(keys + 3) = sl_xor(t3);
			*(keys + 4) = sl_xor(t4);
			*(keys + 5) = sl_xor(t5);
			*(keys + 6) = sl_xor(t6);
			*(keys + 7) = sl_xor(t7);
			t0 = vqtbl1q_u8(t0, R32D);
			t1 = vqtbl1q_u8(t1, R32D);
			t2 = vqtbl1q_u8(t2, R32D);
			t3 = vqtbl1q_u8(t3, R32D);
			t4 = vqtbl1q_u8(t4, R32D);
			t5 = vqtbl1q_u8(t5, R32D);
			t6 = vqtbl1q_u8(t6, R32D);
			t7 = vqtbl1q_u8(t7, R32D);
			SBOX(t0, t1, t2, t3, t4, t5, t6, t7,
				s0, s1, s2, s3, s4, s5, s6, s7);
			s0 = (rcon & 0x01) ? veorq_u8(t0, RCON) : t0;
			s1 = (rcon & 0x02) ? veorq_u8(t1, RCON) : t1;
			s2 = (rcon & 0x04) ? veorq_u8(t2, RCON) : t2;
			s3 = (rcon & 0x08) ? veorq_u8(t3, RCON) : t3;
			s4 = (rcon & 0x10) ? veorq_u8(t4, RCON) : t4;
			s5 = (rcon & 0x20) ? veorq_u8(t5, RCON) : t5;
			s6 = (rcon & 0x40) ? veorq_u8(t6, RCON) : t6;
			s7 = (rcon & 0x80) ? veorq_u8(t7, RCON) : t7;
			rcon <<= 1;
			if (rcon & 0x100) rcon ^= 0x11b;
			t0 = veorq_u8(*keys, s0);
			t1 = veorq_u8(*(keys + 1), s1);
			t2 = veorq_u8(*(keys + 2), s2);
			t3 = veorq_u8(*(keys + 3), s3);
			t4 = veorq_u8(*(keys + 4), s4);
			t5 = veorq_u8(*(keys + 5), s5);
			t6 = veorq_u8(*(keys + 6), s6);
			t7 = veorq_u8(*(keys + 7), s7);
			*keys = t0;
			*(keys + 1) = t1;
			*(keys + 2) = t2;
			*(keys + 3) = t3;
			*(keys + 4) = t4;
			*(keys + 5) = t5;
			*(keys + 6) = t6;
			*(keys + 7) = t7;
			keys += 8;
		}
		break;

	case 256:
		numkeys = 120;
		temp = vld1q_u8(input_key);
		temp = vqtbl1q_u8(temp, M0);
		t0 = vtstq_u8(temp, m1);
		t1 = vtstq_u8(temp, m2);
		t2 = vtstq_u8(temp, m4);
		t3 = vtstq_u8(temp, m8);
		t4 = vtstq_u8(temp, m10);
		t5 = vtstq_u8(temp, m20);
		t6 = vtstq_u8(temp, m40);
		t7 = vtstq_u8(temp, m80);
		*keys = t0;
		*(keys + 1) = t1;
		*(keys + 2) = t2;
		*(keys + 3) = t3;
		*(keys + 4) = t4;
		*(keys + 5) = t5;
		*(keys + 6) = t6;
		*(keys + 7) = t7;
		keys += 8;
		temp = vld1q_u8(input_key + 16);
		temp = vqtbl1q_u8(temp, M0);
		t0 = vtstq_u8(temp, m1);
		t1 = vtstq_u8(temp, m2);
		t2 = vtstq_u8(temp, m4);
		t3 = vtstq_u8(temp, m8);
		t4 = vtstq_u8(temp, m10);
		t5 = vtstq_u8(temp, m20);
		t6 = vtstq_u8(temp, m40);
		t7 = vtstq_u8(temp, m80);
		*keys = t0;
		*(keys + 1) = t1;
		*(keys + 2) = t2;
		*(keys + 3) = t3;
		*(keys + 4) = t4;
		*(keys + 5) = t5;
		*(keys + 6) = t6;
		*(keys + 7) = t7;
		keys += 8;
		rcon = 0x01;
		for (i = 0; i < 6; i++) {
			*keys = sl_xor(*(keys - 16));
			*(keys + 1) = sl_xor(*(keys - 15));
			*(keys + 2) = sl_xor(*(keys - 14));
			*(keys + 3) = sl_xor(*(keys - 13));
			*(keys + 4) = sl_xor(*(keys - 12));
			*(keys + 5) = sl_xor(*(keys - 11));
			*(keys + 6) = sl_xor(*(keys - 10));
			*(keys + 7) = sl_xor(*(keys - 9));
			t0 = vqtbl1q_u8(t0, R32D);
			t1 = vqtbl1q_u8(t1, R32D);
			t2 = vqtbl1q_u8(t2, R32D);
			t3 = vqtbl1q_u8(t3, R32D);
			t4 = vqtbl1q_u8(t4, R32D);
			t5 = vqtbl1q_u8(t5, R32D);
			t6 = vqtbl1q_u8(t6, R32D);
			t7 = vqtbl1q_u8(t7, R32D);
			SBOX(t0, t1, t2, t3, t4, t5, t6, t7,
				s0, s1, s2, s3, s4, s5, s6, s7);
			s0 = (rcon & 0x01) ? veorq_u8(t0, RCON) : t0;
			s1 = (rcon & 0x02) ? veorq_u8(t1, RCON) : t1;
			s2 = (rcon & 0x04) ? veorq_u8(t2, RCON) : t2;
			s3 = (rcon & 0x08) ? veorq_u8(t3, RCON) : t3;
			s4 = (rcon & 0x10) ? veorq_u8(t4, RCON) : t4;
			s5 = (rcon & 0x20) ? veorq_u8(t5, RCON) : t5;
			s6 = (rcon & 0x40) ? veorq_u8(t6, RCON) : t6;
			s7 = (rcon & 0x80) ? veorq_u8(t7, RCON) : t7;
			rcon <<= 1;
			t0 = veorq_u8(*keys, s0);
			t1 = veorq_u8(*(keys + 1), s1);
			t2 = veorq_u8(*(keys + 2), s2);
			t3 = veorq_u8(*(keys + 3), s3);
			t4 = veorq_u8(*(keys + 4), s4);
			t5 = veorq_u8(*(keys + 5), s5);
			t6 = veorq_u8(*(keys + 6), s6);
			t7 = veorq_u8(*(keys + 7), s7);
			*keys = t0;
			*(keys + 1) = t1;
			*(keys + 2) = t2;
			*(keys + 3) = t3;
			*(keys + 4) = t4;
			*(keys + 5) = t5;
			*(keys + 6) = t6;
			*(keys + 7) = t7;
			keys += 8;
			*keys = sl_xor(*(keys - 16));
			*(keys + 1) = sl_xor(*(keys - 15));
			*(keys + 2) = sl_xor(*(keys - 14));
			*(keys + 3) = sl_xor(*(keys - 13));
			*(keys + 4) = sl_xor(*(keys - 12));
			*(keys + 5) = sl_xor(*(keys - 11));
			*(keys + 6) = sl_xor(*(keys - 10));
			*(keys + 7) = sl_xor(*(keys - 9));
			t0 = vqtbl1q_u8(t0, NR32D);
			t1 = vqtbl1q_u8(t1, NR32D);
			t2 = vqtbl1q_u8(t2, NR32D);
			t3 = vqtbl1q_u8(t3, NR32D);
			t4 = vqtbl1q_u8(t4, NR32D);
			t5 = vqtbl1q_u8(t5, NR32D);
			t6 = vqtbl1q_u8(t6, NR32D);
			t7 = vqtbl1q_u8(t7, NR32D);
			SBOX(t0, t1, t2, t3, t4, t5, t6, t7,
				s0, s1, s2, s3, s4, s5, s6, s7);
			t0 = veorq_u8(*keys, t0);
			t1 = veorq_u8(*(keys + 1), t1);
			t2 = veorq_u8(*(keys + 2), t2);
			t3 = veorq_u8(*(keys + 3), t3);
			t4 = veorq_u8(*(keys + 4), t4);
			t5 = veorq_u8(*(keys + 5), t5);
			t6 = veorq_u8(*(keys + 6), t6);
			t7 = veorq_u8(*(keys + 7), t7);
			*keys = t0;
			*(keys + 1) = t1;
			*(keys + 2) = t2;
			*(keys + 3) = t3;
			*(keys + 4) = t4;
			*(keys + 5) = t5;
			*(keys + 6) = t6;
			*(keys + 7) = t7;
			keys += 8;
		}
		*keys = sl_xor(*(keys - 16));
		*(keys + 1) = sl_xor(*(keys - 15));
		*(keys + 2) = sl_xor(*(keys - 14));
		*(keys + 3) = sl_xor(*(keys - 13));
		*(keys + 4) = sl_xor(*(keys - 12));
		*(keys + 5) = sl_xor(*(keys - 11));
		*(keys + 6) = sl_xor(*(keys - 10));
		*(keys + 7) = sl_xor(*(keys - 9));
		t0 = vqtbl1q_u8(t0, R32D);
		t1 = vqtbl1q_u8(t1, R32D);
		t2 = vqtbl1q_u8(t2, R32D);
		t3 = vqtbl1q_u8(t3, R32D);
		t4 = vqtbl1q_u8(t4, R32D);
		t5 = vqtbl1q_u8(t5, R32D);
		t6 = vqtbl1q_u8(t6, R32D);
		t7 = vqtbl1q_u8(t7, R32D);
		SBOX(t0, t1, t2, t3, t4, t5, t6, t7,
			s0, s1, s2, s3, s4, s5, s6, s7);
		s0 = (rcon & 0x01) ? veorq_u8(t0, RCON) : t0;
		s1 = (rcon & 0x02) ? veorq_u8(t1, RCON) : t1;
		s2 = (rcon & 0x04) ? veorq_u8(t2, RCON) : t2;
		s3 = (rcon & 0x08) ? veorq_u8(t3, RCON) : t3;
		s4 = (rcon & 0x10) ? veorq_u8(t4, RCON) : t4;
		s5 = (rcon & 0x20) ? veorq_u8(t5, RCON) : t5;
		s6 = (rcon & 0x40) ? veorq_u8(t6, RCON) : t6;
		s7 = (rcon & 0x80) ? veorq_u8(t7, RCON) : t7;
		*keys = veorq_u8(*keys, s0);
		*(keys + 1) = veorq_u8(*(keys + 1), s1);
		*(keys + 2) = veorq_u8(*(keys + 2), s2);
		*(keys + 3) = veorq_u8(*(keys + 3), s3);
		*(keys + 4) = veorq_u8(*(keys + 4), s4);
		*(keys + 5) = veorq_u8(*(keys + 5), s5);
		*(keys + 6) = veorq_u8(*(keys + 6), s6);
		*(keys + 7) = veorq_u8(*(keys + 7), s7);
		break;

	default:
		return 0;
	}

	return numkeys;
}

inline void aesbs_encryption_round(uint8x16_t *x0, uint8x16_t *x1, uint8x16_t *x2,
	uint8x16_t *x3, uint8x16_t *x4, uint8x16_t *x5, uint8x16_t *x6,
	uint8x16_t *x7, uint8x16_t *bskey)
{
	uint8x16_t t0, t1, t2, t3, t4, t5, t6, t7;
	SBOX(*x0, *x1, *x2, *x3, *x4, *x5, *x6, *x7,
		t0, t1, t2, t3, t4, t5, t6, t7);
	SHIFT_ROWS(*x0, *x1, *x2, *x3, *x4, *x5, *x6, *x7, SR);
	MIX_COLS(*x0, *x1, *x2, *x3, *x4, *x5, *x6, *x7,
		t0, t1, t2, t3, t4, t5, t6, t7);
	*x0 = veorq_u8(*x0, *bskey);
	*x1 = veorq_u8(*x1, *(bskey + 1));
	*x2 = veorq_u8(*x2, *(bskey + 2));
	*x3 = veorq_u8(*x3, *(bskey + 3));
	*x4 = veorq_u8(*x4, *(bskey + 4));
	*x5 = veorq_u8(*x5, *(bskey + 5));
	*x6 = veorq_u8(*x6, *(bskey + 6));
	*x7 = veorq_u8(*x7, *(bskey + 7));
}

#define REPEATS 100000000

int main()
{
	uint8_t ik[16] = {
		0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
		0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
	};
	uint8x16_t bskey[88];
	uint8x16_t block0 = {
		0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
		0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff
	};
	uint8x16_t block1 = {
		0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88,
		0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00
	};
	uint8x16_t block2 = {
		0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99,
		0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00, 0x11
	};
	uint8x16_t block3 = {
		0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa,
		0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00, 0x11, 0x22
	};
	uint8x16_t block4 = {
		0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb,
		0xcc, 0xdd, 0xee, 0xff, 0x00, 0x11, 0x22, 0x33
	};
	uint8x16_t block5 = {
		0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc,
		0xdd, 0xee, 0xff, 0x00, 0x11, 0x22, 0x33, 0x44
	};
	uint8x16_t block6 = {
		0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd,
		0xee, 0xff, 0x00, 0x11, 0x22, 0x33, 0x44, 0x55
	};
	uint8x16_t block7 = {
		0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee,
		0xff, 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66
	};
	time_t t0, t1;
	time(&t0);
	gen_keys(ik, bskey, 128);
	bitslice(&block0, &block1, &block2, &block3, &block4, &block5, &block6, &block7);
	for (uint64_t i = 0; i < REPEATS; i++) {
		aesbs_encryption_round(&block0, &block1, &block2, &block3, &block4, &block5,
			&block6, &block7, &bskey[80]);
	}
	bitslice(&block0, &block1, &block2, &block3, &block4, &block5, &block6, &block7);
	print_vector(block0);
	printf("\n\r");
	print_vector(block1);
	printf("\n\r");
	print_vector(block2);
	printf("\n\r");
	print_vector(block3);
	printf("\n\r");
	print_vector(block4);
	printf("\n\r");
	print_vector(block5);
	printf("\n\r");
	print_vector(block6);
	printf("\n\r");
	print_vector(block7);
	printf("\n\r");
	time(&t1);
	printf("%ld seconds total\n\r", t1 - t0);
	return 0;
}
