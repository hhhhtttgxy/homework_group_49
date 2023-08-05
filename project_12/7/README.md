此处对应的是第7个pitfall（Same d and k with ECDSA, leads to leaking of d）。

|     代码名称     |                        具体实现                         |
| :--------------: | :-----------------------------------------------------: |
|     func.py      |                     共用的密码算法                      |
| ECDSA_Schnorr.py | 实现Schnorr与ECDSA使用相同的随机数k和私钥d会导致d的泄露 |
|   ECDSA_sm2.py   | 实现SM2-sig与ECDSA使用相同的随机数k和私钥d会导致d的泄露 |
