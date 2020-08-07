'''
# Author : 0HP
# Purpose : In algorithm AES
# build S-Box in SubBytes
'''

#multilpy in GF(2^8)
def mul(a,b):
    r=0
    while b:
        if b%2:
            r=r^a #add operation : XOR
        b=b>>1
        if a&int('10000000',2)==0: #first bit's value = 0
            a=a<<1
        else: #first bit's value = 1
            a=a<<1
            a=a^283
    return r
#compute the max index number which < 2^count
#return count, from 0
def highest_bit(n):
    count = 0
    while n:
        count+=1
        n=n>>1
    return count-1
#division about polymerization
#return quotient and remainder
def div(a,b):
    if a==b:
        return 1,0
    if a<b:
        return 0,a
    a_bit = highest_bit(a)
    b_bit = highest_bit(b)
    result = 0
    while not a_bit<b_bit:
        move=a_bit-b_bit
        temp=b<<move
        result=result+(1<<move)
        a=a^temp
        a_bit=highest_bit(a)
    return result,a
#compute the inverse about a', where a*a'=1(mod m)
#the algorithrm likes EGCD
def inverse(a,m):
    r0,s0,r1,s1=1,0,0,1
    while m>0:
        t=m
        q,m=div(a,m)#q=a//m,m=a mod m
        a=t#a=m
        r0,r1=r1,r0^mul(q,r1)#sub operation:XOR
        s0,s1=s1,s0^mul(q,s1)
    return r0 #a'

#build the matrix  to multiply b0-b7 in step 3
def build_T(T_value):
    T_List=[]
    for i in range(8):
        T_List.append(T_value)
        if T_value&1:
            T_value=(T_value>>1)^int('10000000',2)
        else:
            T_value=T_value>>1
    return T_List

#compute every value's inverse in a matrix
def S_inverse(S):
    for i in range(len(S)):
        for j in range(len(S[0])):
            S[i][j]=inverse(S[i][j],283)
    return S

def build_byte_order_S(S):
    for i in range(len(S)):
        for j in range(len(S[0])):
            S[i][j]=(i<<4)+j
    return S

def Compute_S_Box(T,S,c):
    for i in range(len(S)):
        for j in range(len(S[0])):
            # In order to multiply matrix T,let every bit in a byte reverse.
            Bit=list('{:08b}'.format(S[i][j]))
            Bit.reverse()
            Bit_s=""
            for k in Bit:
                Bit_s=Bit_s+str(k)
            Bit=int(Bit_s,2)
            # T */& b0-b7
            T_result=[]
            for l in T:
                And=l&Bit
                And_list=list('{:08b}'.format(And))
                And_reslut=int(And_list[0],2)
                for m in And_list[1:]:
                    And_reslut=And_reslut^int(m,2)
                T_result.append(And_reslut)
            T_result_s=""
            for n in T_result:
                T_result_s=T_result_s+str(n)
            # get the reslut +/XOR c/63's reverse bits
            S_temp=int(T_result_s,2)^c
            S_temp=list('{:08b}'.format(S_temp))
            S_temp.reverse()#reverse again, get the final answer
            S_temp_s=""
            for o in S_temp:
                S_temp_s=S_temp_s+str(o)
            S[i][j]=int(S_temp_s,2)
    return S

T=[]
T_v=143
c=int('11000110',2)
S1=[[0]*16 for i in range(16)]#S_Box
S1=build_byte_order_S(S1)
S1=S_inverse(S1)
T=build_T(T_v)
S1=Compute_S_Box(T,S1,c)

def SubByte(n:int):
    high_four=(n&int('11110000',2))>>4
    low_four=(n&int('00001111',2))
    return S1[high_four][low_four]