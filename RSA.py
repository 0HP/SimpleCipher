'''
# Author: 0HP
# RSA: Encrypt,Decrypt,Signatrue,Auth
'''
import ComFunc
import hashlib
import copy
from multiprocessing import Process
from multiprocessing.pool import Pool
import multiprocessing
import time
import os

class RSA:
    __m = b""
    __mlist = []
    __e,__d,__n=0,0,0

    def GetPlain(self,filename):
        if filename=="":
            exit(1)
        with open(filename,"rb") as f:
            self.__m = f.read()

    def GetPuKey(self,filename):
        if filename=="":
            exit(1)
        rf=open(filename,"r",encoding="utf-8")
        l = []
        for i in rf.readlines():
            l.append(int(i))
        if not len(l)==2:
            exit(1)
        self.__e,self.__n = l[0],l[1]

    def GetPrKey(self,filename):
        if filename=="":
            exit(1)
        rf=open(filename,"r",encoding="utf-8")
        l = []
        for i in rf.readlines():
            l.append(int(i))
        if not len(l)==2:
            exit(1)
        self.__d,self.__n = l[0],l[1]

    #if massage's length > 1024/2048 bits
    #need block (every block 1024/2048 bytes)
    #Plain block has 1024bit(128bytes), Crypher block has 2048bits(256bytes)
    def BlockMessage(self,bytelen):
        tmp=self.__m
        while len(tmp)>bytelen:
            self.__mlist.append(tmp[0:bytelen])
            tmp=tmp[bytelen:]
        if len(tmp)>0:
            self.__mlist.append(tmp)

    #RSA Encrypt Algorithm
    def Encrypt(self,savefile):
        if len(self.__mlist) <1 or self.__e==0 or self.__n==0:
            exit(1)
        if savefile=="":
            exit(1)

        CipherList = []
        ParaList = []
        for i in self.__mlist:
            ParaList.append([int.from_bytes(i,'big'),self.__e,self.__n])

        pool = Pool(processes=4)
        CipherList = pool.map(ComFunc.RSAPow,ParaList)
        pool.close()
        pool.join()
        '''
        for i in self.__mlist:
            Num = int.from_bytes(i,'big')
            CipherList.append(ComFunc.QPow(Num,self.__e,self.__n))
        '''

        with open(savefile,"wb") as fw:
            for i in CipherList:
                fw.write(i.to_bytes(256, 'big'))

        return True

    #RSA Decrypt Algorithm
    def Decrypt(self,savefile):
        if len(self.__mlist) <1 or self.__d==0 or self.__n==0:
            exit(1)
        if savefile=="":
            exit(1)

        PlainList = []
        QPowPara = []
        for i in self.__mlist:
            QPowPara.append([int.from_bytes(i,'big'),self.__d,self.__n])
        pool = Pool(processes=4)
        PlainList = pool.map(ComFunc.RSAPow,QPowPara)
        pool.close()
        pool.join()

        fw = open(savefile,"wb")
        for i in PlainList:
            tmpi = i
            bitlen = len(bin(tmpi)[2:])
            bytelen = 0
            if bitlen%8 == 0:
                bytelen = bitlen//8
            else:
                bytelen = bitlen//8+1
            fw.write(i.to_bytes(bytelen,'big'))
        fw.close()
        return True

    def SignNature(self,filename,savefile):
        if filename=="" or savefile == "":
            exit(1)
        if self.__d==0 or self.__n==0:
            exit(1)

        fr = open(filename,"rb")
        M = fr.read()
        fr.close()

        MHash = hashlib.sha3_256()
        MHash.update(M)
        HashInt = int(MHash.hexdigest(),16)

        Sign = ComFunc.QPow(HashInt,self.__d,self.__n)

        fw = open(savefile,"wb")
        fw.write(Sign.to_bytes(256,'big'))
        fw.close()
        return True

    def Auth(self,SignFile,filename):
        if filename=="" or SignFile == "":
            exit(1)
        if self.__e==0 or self.__n==0:
            exit(1)

        fr = open(SignFile,"rb")
        Sign = fr.read()
        fr.close()

        SignInt = int.from_bytes(Sign,'big')
        HashInt = ComFunc.QPow(SignInt,self.__e,self.__n)

        fr = open(filename,"rb")
        m = fr.read()
        fr.close()

        MHash = hashlib.sha3_256()
        MHash.update(m)

        if int(MHash.hexdigest(),16) == HashInt:
            return True
        else:
            return False


if __name__ == '__main__':
    RSAOJ=RSA()
    RSAOJ.GetPrKey("prkey.txt")
    RSAOJ.GetPuKey("pukey.txt")
    RSAOJ.GetPlain("c.txt")
    RSAOJ.BlockMessage(256)
    starttime = time.time()
    RSAOJ.Decrypt("aa.mp3")
    endtime = time.time()
    print(endtime - starttime)

#RSAOJ.SignNature("a.mp3","s.txt")
#if RSAOJ.Auth("s.txt","a.mp3"):
#    print("ok")

