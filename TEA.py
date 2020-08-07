import sys
import getopt

class TEA:

    #秘钥
    __Key=[]
    #CBC模式的初始向量
    __CBCVI=[]
    #Counter模式的计数器
    __Count=[]
    #读出的明文
    __P=""
    #对明文填充分组
    __Plain=[]
    #待写入的文件
    __File=""
    #加密模式选择
    __Module=""
    #从文件中读取秘钥
    def ReadKey(self,KeyFile):
        if KeyFile=="":
            exit()
        fr=open(KeyFile,"r",encoding='utf-8')
        #以十六进制读取秘钥
        for i in fr.readlines():
            self.__Key.append(int(i,16)&2**32-1)#保证秘钥是32比特
        fr.close()

    #读文件
    def ReadFile(self,Rfile):
        if Rfile=="":
            exit(1)
        f=open(Rfile,'rb')
        self.__P=f.read()
        f.close()

    #写入文件的文件名
    def WriteFile(self,filename):
        if filename=="":
            exit(1)
        self.__File=filename

    #选择加密模式
    def SelectModule(self,m):
        self.__Module=m

    #计数器初始值
    def ReadCount(self,CountFile):
        if CountFile=="":
            exit(1)
        with open(CountFile,'r',encoding='utf-8') as f:
            for i in f.readlines():
                self.__Count.append(int(i,16))

    #CBC初始向量
    def ReadVI(self,VIFile):
        if VIFile=="":
            exit(1)
        with open(VIFile,'r',encoding='utf-8') as f:
            for i in f.readlines():
                self.__CBCVI(int(i,16))

    #采用PSK7填充方法
    def Padding(self):
        #每一组64位，8个字节
        #若是刚好可整除8，补充8个字节
        if len(self.__P)%8==0:
            self.__P=self.__P+b'\x08'*8
        else:
            l=[b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08']
            PadLen=8-(len(self.__P)%8)
            self.__P=self.__P+l[PadLen-1]*PadLen

    #对明文分组，每8个字节分为1组
    def BlockPlain(self):
        i=0
        while i<len(self.__P):
            self.__Plain.append(self.__P[i:i+8])
            i=i+8

    #TEA加密，v是两个32位整型数的列表
    def TEA(self,v):
        int32=2**32-1
        v0,v1=v[0]&int32,v[1]&int32
        delta,Sum=0x9e3779b9,0
        for i in range(32):
            Sum=(Sum+delta)&int32
            v0=(v0+(((v1<<4)+self.__Key[0])^(v1+Sum)^((v1>>5)+self.__Key[1])))&int32
            v1=(v1+(((v0<<4)+self.__Key[2])^(v0+Sum)^((v0>>5)+self.__Key[3])))&int32
        v[0],v[1]=v0,v1
        return v

    #TEA的解密算法
    def TEADe(self,v):
        int32=2**32-1
        v0, v1 = v[0] & int32, v[1] & int32
        delta, Sum = 0x9e3779b9, 0xc6ef3720
        for i in range(32):
            v1=(v1-(((v0<<4)+self.__Key[2])^(v0+Sum)^((v0>>5)+self.__Key[3])))&int32
            v0=(v0-(((v1<<4)+self.__Key[0])^(v1+Sum)^((v1>>5)+self.__Key[1])))&int32
            Sum=(Sum-delta)&int32
        v[0],v[1]=v0,v1
        return v

    #TEA的CBC模式加密，结果写入文件中
    def TEACryptCBC(self,RFile):
        if not self.__Module=="1":
            return False
        #记录待加密整数的列表
        VP=[]
        self.ReadFile(RFile)
        self.Padding()
        self.BlockPlain()
        for i in self.__Plain:
            Num0,Num1,index=0,0,0
            while index<4:
                Num0=(Num0<<8)+i[index]
                index+=1
            while index>=4 and index<8:
                Num1=(Num1<<8)+i[index]
                index+=1
            VP.append([Num0,Num1])
        VPIndex=0
        while VPIndex<len(VP):
            #异或
            InputV=[VP[VPIndex][0]^self.__CBCVI[0],VP[VPIndex][1]^self.__CBCVI[1]]
            #加密函数
            VP[VPIndex]=self.TEA(InputV)
            #下一个与分组异或的向量
            self.__CBCVI[0],self.__CBCVI[1]=VP[VPIndex][0],VP[VPIndex][1]
            VPIndex+=1


        #得到密文分组VP[[]],写入文件
        fw=open(self.__File,"wb")
        for i in VP:
            fw.write(i[0].to_bytes(4,'big'))
            fw.write(i[1].to_bytes(4,'big'))
        fw.close()
        return True

    #TEA的CBC模式解密，结果写入文件中
    def TEADecryCBC(self,RFile):
        if not self.__Module=='1':
            return False
        self.ReadFile(RFile)
        self.BlockPlain()
        CryptText=[]
        DecryText=[]

        for i in self.__Plain:
            Num0,Num1,index=0,0,0
            while index<4:
                Num0=(Num0<<8)+i[index]
                index+=1
            while index>=4 and index<8:
                Num1=(Num1<<8)+i[index]
                index+=1
            CryptText.append([Num0,Num1])
        Cindex=0

        while Cindex<len(CryptText):
            TmpP=[0,0]
            TmpP[0],TmpP[1]=CryptText[Cindex][0],CryptText[Cindex][1]
            TmpP=self.TEADe(TmpP)
            TmpP[0],TmpP[1]=TmpP[0]^self.__CBCVI[0],TmpP[1]^self.__CBCVI[1]
            DecryText.append(TmpP)
            self.__CBCVI[0],self.__CBCVI[1]=CryptText[Cindex][0],CryptText[Cindex][1]
            Cindex+=1

        DeBin=b''
        for i in DecryText:
            DeBin=DeBin+i[0].to_bytes(4,'big')+i[1].to_bytes(4,'big')

        #去除填充的比特
        DeleteNum=DeBin[-1]
        DeBin=DeBin[:-DeleteNum]

        fw=open(self.__File,'wb')
        fw.write(DeBin)
        fw.close()
        return True

    #TEA的Counter模式加密，结果写入文件中
    def TEACryptCounter(self,RFile):
        if not self.__Module=="0":
            return False

        self.ReadFile(RFile)
        #记录待加密整数的列表
        VP=[]
        self.Padding()
        print(self.__P)
        self.BlockPlain()
        for i in self.__Plain:
            Num0,Num1,index=0,0,0
            while index<4:
                Num0=(Num0<<8)+i[index]
                index+=1
            while index>=4 and index<8:
                Num1=(Num1<<8)+i[index]
                index+=1
            VP.append([Num0,Num1])

        VPIndex=0
        while VPIndex<len(VP):
            #对计数器值加密
            CryCount=[0,0]
            CryCount[0],CryCount[1]=self.__Count[0],self.__Count[1]
            CryCount=self.TEA(CryCount)
            VP[VPIndex][0],VP[VPIndex][1]=VP[VPIndex][0]^CryCount[0],VP[VPIndex][1]^CryCount[1]
            self.__Count[0],self.__Count[1]=self.__Count[0]+1,self.__Count[1]+1
            VPIndex+=1
        fw=open(self.__File,"wb")
        for i in VP:
            fw.write(i[0].to_bytes(4,'big'))
            fw.write(i[1].to_bytes(4,'big'))
        fw.close()
        return True

    #TEA的Counter模式解密，结果写入文件中
    def TEADecryCounter(self,RFile):
        if not self.__Module=="0":
            return False

        self.ReadFile(RFile)
        self.BlockPlain()

        CryptText=[]
        DecryText=[]

        for i in self.__Plain:
            Num0,Num1,index=0,0,0
            while index<4:
                Num0=(Num0<<8)+i[index]
                index+=1
            while index>=4 and index<8:
                Num1=(Num1<<8)+i[index]
                index+=1
            CryptText.append([Num0,Num1])

        Cindex=0
        while Cindex<len(CryptText):
            Counter=[0,0]
            Counter[0],Counter[1]=self.__Count[0],self.__Count[1]
            Counter=self.TEA(Counter)
            Counter[0],Counter[1]=Counter[0]^CryptText[Cindex][0],Counter[1]^CryptText[Cindex][1]
            DecryText.append(Counter)
            self.__Count[0],self.__Count[1]=self.__Count[0]+1,self.__Count[1]+1
            Cindex=Cindex+1

        DeBin=b''
        for i in DecryText:
            DeBin=DeBin+i[0].to_bytes(4,'big')+i[1].to_bytes(4,'big')

        #去除填充的比特
        print(DeBin)
        DeleteNum=DeBin[-1]
        DeBin=DeBin[:-DeleteNum]

        fw=open(self.__File,'wb')
        fw.write(DeBin)
        fw.close()
        return True