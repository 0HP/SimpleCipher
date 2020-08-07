'''
# Author : 0HP
# Purpose : In algorithm AES (Step 3)
# Mix Colunm
'''
import AES_SBox


#Multiply two matrix in GF(2^8)
#matrix a and b have same rank, and thay are normal matrix, meaning row=colunm
def Matrix_Mul(a,b):
    row=len(a)
    c=[[0,0,0,0] for i in range(4)]
    for i in range(row):
        for j in range(row):#row=colunm
            k=0
            while k<row:
                c[i][j]=c[i][j]^(AES_SBox.mul(a[i][k],b[k][j]))
                k+=1
    return c

MixMatrix = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
