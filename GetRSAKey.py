'''
# Author: 0HP
# Get Public Key and Private Key in RSA
# Save them to two file
# file will be named by user
'''
import GetPrime
import ComFunc

def CreateKey(e,pufile,prfile):
    p,q=GetPrime.Build_Prime(e)
    n=p*q
    Phi_n=(p-1)*(q-1)
    d=ComFunc.egcd(e,Phi_n)

    # write public key to a file
    puf=open(pufile,"w+")
    puf.write(str(e)+'\n')
    puf.write(str(n))
    puf.close()

    prf=open(prfile,"w+")
    prf.write(str(d)+'\n')
    prf.write(str(n))
    prf.close()

CreateKey(65537,"pukey.txt","prkey.txt")