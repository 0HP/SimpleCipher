'''
# Author : 0HP
# AES Algorithm (CTR Module)
'''
import AES_SBox
import AES_ShiftRow
import AES_MixColunm
import AES_AddRoundKey
from multiprocessing import Process
import multiprocessing
from multiprocessing.pool import Pool
import os
import time

class AES:
    __Key = 0
    __Counter = 0
    __CountList = []
    __M = b''
    __MList = []
    __PadNum = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x04',b'\x05', b'\x06',b'\x07',
                b'\x08', b'\x09', b'\x0a', b'\x0b', b'\x0c', b'\x0d',b'\x0e', b'\x0f']

    __W = [] #len = 11

    def GetKey(self,KeyFile):
        fr = open(KeyFile,'r',encoding='utf-8')
        KeyStr = fr.read()
        fr.close()
        self.__Key = int(KeyStr,16)

    def ExpanKey(self):
        if self.__Key == 0:
            exit(1)
        W = AES_AddRoundKey.KeyExpansion(self.__Key)
        Index = 0
        while Index<44:
            self.__W.append((W[Index]<<96)+(W[Index+1]<<64)+(W[Index+2]<<32)+W[Index+3])
            Index += 4

    def GetCounter(self,CounterFile):
        fr = open(CounterFile, 'r', encoding='utf-8')
        CounterStr = fr.read()
        fr.close()
        self.__Counter = int(CounterStr, 16)

    '''
    def GenSBox(self):
        self.__SBox = [[0]*16 for i in range(16)]
        self.__SBox = AES_SBox.build_byte_order_S(self.__SBox)
        self.__SBox = AES_SBox.S_inverse(self.__SBox)
        T = []
        T = AES_SBox.build_T(self.__Tv)
        self.__SBox = AES_SBox.Compute_S_Box(T,self.__SBox,self.__C)
    
    def SubByte(self,n:int):
        if len(self.__SBox)<2:
            exit(1)
        high_four = (n&int('11110000',2))>>4
        low_four = (n&int('00001111',2))
        return self.__SBox[high_four][low_four]
    '''
    def GetPlain(self,filename):
        if filename == "":
            exit(1)
        fr = open(filename,'rb')
        self.__M = fr.read()
        fr.close()

    #let message could mod 16bytes
    def Padding(self):
        if len(self.__M)%16 == 0:
            self.__M = self.__M + self.__PadNum[0]*16
        else:
            PadLen = 16 - (len(self.__M)%16)
            self.__M = self.__M + self.__PadNum[PadLen]*PadLen

    #every block include 16bytes/128bits
    def BlockMessage(self):
        if len(self.__M) == 0 or len(self.__M)%16!=0:
            exit(1)
        tmp = self.__M
        while len(tmp)>16:
            self.__MList.append(tmp[0:16])
            tmp = tmp[16:]
        if len(tmp)>0:
            self.__MList.append(tmp)

    def Encrypt(self,savefile):
        if savefile=="" or len(self.__MList)==0:
            exit(1)
        TmpCount = self.__Counter
        for i in range(len(self.__MList)):
            self.__CountList.append(TmpCount)
            TmpCount+=1

        '''
        print(self.__CountList)
        for i in range(len(self.__CountList)):
            self.__CountList[i] = AES_AddRoundKey.CRT(self.__CountList[i],self.__W)

        print(self.__CountList)
        for i in range(len(self.__CountList)):
            self.__CountList[i] = self.__CountList[i]^(int.from_bytes(self.__MList[i],'big'))
        '''

        CRTPara = []
        for i in range(len(self.__CountList)):
            CRTPara.append([self.__CountList[i],self.__W])
        XorPara = []

        pool = Pool(processes=4)
        self.__CountList = pool.map(AES_AddRoundKey.CRTMap, CRTPara)
        pool.close()
        pool.join()

        for i in range(len(self.__CountList)):
            XorPara.append([self.__CountList[i],int.from_bytes(self.__MList[i],'big')])

        pool = Pool(processes=4)
        CipherList = pool.map(AES_AddRoundKey.funcXor, XorPara)
        pool.close()
        pool.join()


        with open(savefile, "wb") as fw:
            for i in CipherList:
                fw.write(i.to_bytes(16, 'big'))
        return True

    def Decrypt(self,savefile):
        if savefile=="" or len(self.__MList)==0:
            exit(1)
        TmpCount = self.__Counter
        for i in range(len(self.__MList)):
            self.__CountList.append(TmpCount)
            TmpCount+=1

        CRTPara = []
        for i in range(len(self.__CountList)):
            CRTPara.append([self.__CountList[i],self.__W])
        XorPara = []

        pool = Pool(processes=4)
        self.__CountList = pool.map(AES_AddRoundKey.CRTMap, CRTPara)
        pool.close()
        pool.join()

        for i in range(len(self.__CountList)):
            XorPara.append([self.__CountList[i],int.from_bytes(self.__MList[i],'big')])

        pool = Pool(processes=4)
        PlainList = pool.map(AES_AddRoundKey.funcXor, XorPara)
        pool.close()
        pool.join()

        PlainByte = b''
        for i in PlainList:
            PlainByte = PlainByte + i.to_bytes(16,'big')
        PadLen = PlainByte[-1]
        if PadLen==0:
            PlainByte = PlainByte[:-16]
        else:
            PlainByte = PlainByte[:-PadLen]

        with open(savefile, "wb") as fw:
            fw.write(PlainByte)
        return True


if __name__ == '__main__':
    AESOJ = AES()
    AESOJ.GetKey("AESKey.txt")
    AESOJ.ExpanKey()
    AESOJ.GetCounter("Counter.txt")
    AESOJ.GetPlain("c1.txt")
    AESOJ.BlockMessage()
    starttime = time.time()
    AESOJ.Decrypt("d1.txt")
    endtime = time.time()
    print(endtime - starttime)