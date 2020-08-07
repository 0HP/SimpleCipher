'''
# Author: 0HP
# Commom Function to compute somethings
# Include Quick_Multiply, Quick_Power (mod n)
# GCD EGCD
'''

#Algorithm GCD to compute greatest common divisor
def gcd(a,b):
    while b!=0:
        y=b
        b=a%b
        a=y
    return a


def egcd(a,b):
    r0,r1,s0,s1,t=1,0,0,1,b
    while b:
        q,a,b=a//b,b,a%b
        r0,r1=r1,r0-q*r1
        s0,s1=s1,s0-q*s1
    if r0<0:
        r0=r0%t
    return r0

#A quickly multiply algorithm with modding n
def Qmul(a,b,n):
    r=0
    while b:
        if b&1:
            r=(r+a)%n
        b=b>>1
        a=(a<<1)%n
    return r

#A quidckly exponential algorithm with modding n
def QPow(a,x,n):
    result=1
    while x:
        if x&1:
            result=(result*a)%n
        x=x>>1
        a=(a*a)%n
    return result

def RSAPow(l):
    return QPow(l[0],l[1],l[2])