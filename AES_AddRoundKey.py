'''
# Author : 0HP
# Purpose : In algorithm AES (Step 4)
'''
import AES_ShiftRow
import AES_SBox
import AES_MixColunm
import os

RC=[1,2,4,8,16,32,64,128,int('1b',16),int('36',16)]

#w:int, 4bytes
#return int w' 4bytes
def g_function(w:int,KeyRound):
    B = []
    W = w.to_bytes(4,'big')
    Index = 0
    for i in W:
        B.append(i)
    B = AES_ShiftRow.ShiftRow_Left_One(B)
    for i in range(len(B)):
        B[i] = AES_SBox.SubByte(B[i])
    B[0] = B[0] ^ RC[KeyRound]
    return (B[0]<<24)+(B[1]<<16)+(B[2]<<8)+B[3]

#key:int,16bytes
#return W,list ,include 44 value,every value is 4bytes int
def KeyExpansion(key:int):
    Key = key.to_bytes(16,'big')
    W = []
    for i in range(4):
        W.append((Key[4*i]<<24)+(Key[4*i+1]<<16)+(Key[4*i+2]<<8)+Key[4*i+3])
    for i in range(10):
        Wg = g_function(W[-1],i)
        W_new = Wg ^ W[len(W)-4]
        W.append(W_new)
        for j in range(3):
            W.append(W[-1]^W[len(W)-1])
    return W

#state: 4*4 Matrix, int type;key: 16bytes int
#return a new Matrix
def AddRoundKey(state,key):
    P = 0
    for i in range(4):
        for j in range(4):
            P = (P<<8) + state[i][j]
    NewP = P ^ key
    NewByte = NewP.to_bytes(16,'big')
    NewState = [[0, 0, 0, 0] for i in range(4)]
    Index = 0
    for i in range(4):
        for j in range(4):
            NewState[i][j] = NewByte[Index]
            Index+=1
    return NewState


def funcXor(l):
    return l[0]^l[1]

def CRT(Counter:int,W):
    state = [[0, 0, 0, 0] for i in range(4)]
    CountByte = Counter.to_bytes(16,'big')
    CountIndex = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] = CountByte[CountIndex] #int type
            ++CountIndex

    #10 Rounds Encrypt

    # step4: AddRoundKey
    state = AddRoundKey(state, W[0])
    for t in range(9):
        #step1: SubByte
        for i in range(len(state)):
            for j in range(len(state[0])):
                state[i][j] = AES_SBox.SubByte(state[i][j])

        #step2: ShiftRow
        state = AES_ShiftRow.ShiftRow_Left_All(state)

        #step3: MixColunm
        state = AES_MixColunm.Matrix_Mul(AES_MixColunm.MixMatrix,state)

        #step4: AddRoundKey
        state = AddRoundKey(state,W[t+1])

    # step1: SubByte
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] = AES_SBox.SubByte(state[i][j])
    # step2: ShiftRow
    state = AES_ShiftRow.ShiftRow_Left_All(state)
    # step4: AddRoundKey
    state = AddRoundKey(state, W[10])

    NewCount = 0
    for i in range(4):
        for j in range(4):
            NewCount = (NewCount<<8) + state[i][j]
    return NewCount

def CRTMap(l:list):
    return CRT(l[0],l[1])
