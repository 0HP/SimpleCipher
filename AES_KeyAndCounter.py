'''
# Author : 0HP
# Purpose : In algorithm AES (Step 4)
# Generate Key and Counter Number
'''
import codecs
import random

def BuildRandomKey(n):
    number=random.randint(0,1)
    while n-1:
        number=(number<<1)|random.randint(0,1)
        n=n-1
    return number


#generate Key
fk=codecs.open("AESKey.txt","w")
fk.write(hex(BuildRandomKey(128))[2:])
fk.close()

#generate counter
fc=codecs.open("Counter.txt","w")
fc.write(hex(BuildRandomKey(128))[2:])
fc.close()
