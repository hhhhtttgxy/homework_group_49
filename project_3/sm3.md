# 实现SM3算法
## 1. 实现过程
参照官方文档完成实现
http://www.sca.gov.cn/sca/xwdt/2010-12/17/1002389/files/302a3ada057c4a73830536d03e683110.pdf
## 2. 实现验证
- 填充后的消息：

![image](./image/828bccb0-5455-4d05-8dff-8430aae024b1.png)


- 第一个消息分组扩展后的消息：

![image](./image/96cdddba-a9d2-4390-9564-41132fe4bd12.png)

- 第一个消息分组迭代压缩中间值（部分）：

![image](./image/1518a23e-4e0a-434f-862d-f16a22de2291.png)

- 第二个消息分组扩展后的消息：

![image](./image/4fd29c03-c3b3-449d-b392-ce41a9855606.png)

- 第二个消息分组迭代压缩中间值（部分）：

![image](./image/935df951-e152-430b-a5cd-1de03e9091a9.png)

- 最终压缩结果：

![image](./image/395012e7-32f8-43c2-8940-d790b8e3407f.png)

经验证，中间过程与结果均与官方文档一致。

## 3. 实现效率
![image](./image/65b97991-1589-4b02-a33d-cbc4d9becec7.png)
