# send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself
## 1. 实现原理
Bitcoin测试网（Bitcoin Testnet）是比特币的一个测试网络，旨在供开发人员和用户测试新的比特币应用程序或交易，而不必使用真正的比特币和区块链。与比特币主网相比，比特币测试网的区块链大小要小得多。目前，比特币测试网的区块链大小约为6 GB左右。由于测试网的使用相对较少，因此其区块链增长速度较慢。

![image](./image/3cecd2bc-6ee0-48c8-9b02-ddab130e8a46.png)


> ![image](./image/328601a8-d23d-4a47-8244-1336589da30f.png)
>
> ![image](./image/4f79052d-5ef1-430c-9776-1aa9f6b3dd53.png)
>
> ![image](./image/60ac07f2-40f3-4c31-bf2d-912183169ec7.png)
>
> ![image](./image/2a08f26e-7e29-42ee-b7fb-381f576eceda.png)




## 2. 实现过程

- 使用bitcoin core的测试版（参考文献[2]），下载完成后还需要先同步数据。

![image](./image/23a29bcf-d444-453b-9479-baa857bfb0d9.png)

- 首先需要建一个收款地址，也就是说别人可以通过这个地址向我提供比特币。

![image](./image/8b639c34-e104-45b8-88f9-5ede26caf207.png)

地址：tb1q6hcld6z7zcjpekxg2h56xs9kj80vuy3xu8rg7u

- 当然实际上是使用Testnet（参考文献[3]）向自己发送比特币，最终发送成功，我也成功收到。

![image](./image/59d39f9f-688f-4c3b-8c42-ad9832a7b271.png)

![image](./image/f2c6c322-982c-475f-a43c-2a44515c2613.png)

![image](./image/13b68b9d-8bca-4632-8da8-76e2cd0c7a88.png)

- 对交易数据进行解析，并获取交易的hex（参考文献[4]）。

![image](./image/7691df69-0863-4846-a3b2-d7d0d77199d1.png)

![image](./image/845c9912-e28b-4d98-92dc-a534ed042611.png)


- 最终将测试币返还。

## 参考文献

[1] https://en.bitcoin.it/wiki/Testnet

[2] https://bitcoin.org/zh_CN/download

[3] http://bitcoinfaucet.uo1.net/send.php

[4] https://mempool.space/testnet/docs/api/rest#get-transaction

[5] https://aandds.com/blog/bitcoin-tx.html

[6] https://en.bitcoin.it/wiki/Protocol_documentation#tx
