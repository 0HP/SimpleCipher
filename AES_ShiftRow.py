'''
# Author : 0HP
# Purpose : In algorithm AES (Step 2)
'''

#S : [[]] , int type
def ShiftRow_Left_One(S):
    temp=S[0]
    for i in range(len(S)-1):
        S[i]=S[i+1]
    S[len(S)-1]=temp
    return S

def ShiftRow_Left_All(S):
    for i in range(len(S)):
        for j in range(i):
            S[i]=ShiftRow_Left_One(S[i])
    return S