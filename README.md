# SimpleCipher

>实现对任意文件的 加密/解密/签名/认证功能的命令行程序
---
## 0加密解密算法
### 0.0对称加密（AES与TEA）
AES算法采用CTR模式，分组128bits，计算Counter值和密文时，采用多进程并行计算 

AES四个步骤的实现分别对应于文件：

AES_SBox.py，AES_ShiftRow.py，AES_MixColunm.py，AES_AddRoundKey.py
快速生成随机bits秘钥和计数器值在文件AES_KeyAndCounter.py中

TEA算法可选CTR模式或者CBC模式
算法实现在文件TEA.py中

### 0.1非对称加密（RSA）
采用安全参数为2048bits（模数大小）的分组

生成1024bits素数对基于米勒拉宾素数测试算法
生成算法在文件GetPrime.py

秘钥生成在文件GetRSAKey.py中，公钥e默认65537

欧几里得算法、拓展欧几里得算法、快速模乘法、快速模幂算法在文件ComFunc.py

算法实现在文件RSA.py中，加解密计算采用多进程并行计算

## 1签名/认证
签名/认证采用RSA算法，哈希函数采用SHA3-256
