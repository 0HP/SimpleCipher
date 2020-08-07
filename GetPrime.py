'''
# Author: 0HP
# get two 1024bits prime
# using MillerRabin Algorithm
'''
import ComFunc
import random

#Find the number = (n-1)/2^k
def Find_q(n):
    while not n&1:
        n=n>>1
    return n

#Miller Rabin algorithm
def Miller_Rabin(a,n):
    q=Find_q(n-1)
    aq=ComFunc.QPow(a,q,n)
    #final condition,q=n-1
    while q<n:
        if aq==1 or aq==-1:
            return True
        #make aq = aq(q*2^j)
        aq=ComFunc.QPow(aq,2,n)
        q=q<<1
    return False

#A quickly algorithm to make a odd number
def Build_Random_Odd(nbit):
    #hightest bit = 1
    number=1
    #every bit value = 0 or 1
    while nbit-2:
        number=(number<<1)|random.randint(0,1)
        nbit=nbit-1
    #lowest bit = 1, make it is odd
    number=(number<<1)|1
    return number

#A algorithm to test whether a number is a prime
def Judge_Prime(n):
    #using Miller Rabin to test is in 10 times
    t=10
    while t:
        t-=1
        a=random.randint(2,n-1)
        if not Miller_Rabin(a,n):
            return False
    return True

#A algrothm to build prime p and q, and gcd(e,Phi(n))=1
#because Phi(n)=(p-1)*(q-1), if gcd(e,Phi(n))!=1, e must be the factor with p-1 or q-1
def Build_Prime(e):
    while True:
        i=0
        p_flag=False
        p_bit=random.randint(512,1024)
        p=Build_Random_Odd(p_bit)
        #if it is not a prime, maybe it plus 2 will be
        #try 100 times, meaning plus 100
        while i<100:
            if Judge_Prime(p):
                p_flag=True
                break
            else:
                p=p+2
                i+=1
                continue
        #if (p-1) don't coprime e, make another p again
        if p_flag and ComFunc.gcd(e,p-1)==1:
            break
        else:
            continue
    while True:
        j=0
        q_flag=False
        q_bit=random.randint(512,1024)
        q=Build_Random_Odd(q_bit)
        while j<100:
            if Judge_Prime(q):
                q_flag=True
                break
            else:
                q=q+2
                j+=1
                continue
        if q_flag and ComFunc.gcd(e,q)==1:
            break
        else:
            continue
    return p,q
