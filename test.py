import struct
import ComFunc
import hashlib
import threading
from multiprocessing import Pool
import os
'''
f=open("p.txt","rb")
sf=f.read()
f.close()

m=int.from_bytes(sf,'big')
fw=open("c.txt","wb")
fw.write(m.to_bytes(2,'big'))
fw.close()
'''
'''
m = 11
rf0=open("pukey.txt","r",encoding="utf-8")
l0 = []
for i in rf0.readlines():
    l0.append(int(i))
e, n = l0[0], l0[1]
rf0.close()
rf=open("prkey.txt","r",encoding="utf-8")
l = []
for i in rf.readlines():
    l.append(int(i))
d, n = l[0], l[1]
rf.close()

c=ComFunc.QPow(m,e,n)
print(ComFunc.QPow(c,d,n))
'''
'''
MHash = hashlib.sha3_256()
MHash.update(b'')
print(MHash.hexdigest())
'''
l=[i for i in range(20)]
def inc(n):
    l[n]=l[n]+1
    return l[n]

for i in range(5):
    threading.Thread(target=inc, args=(i,)).start()


def func(i):
    print(i)


def pf():
    pool = Pool(processes=3)
    pool.map(func,[1,2,3,4,5])
    pool.close()
    pool.join()

if __name__ == "__main__":
    pf()
    print(105311069567371524887032370059464416438^int.from_bytes(b'11\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e','big'))


