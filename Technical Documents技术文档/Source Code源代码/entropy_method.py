import numpy as np
import pandas as pd
import xlrd

def shangquanfa(D):
    #D的第一行放指标，其余行放公司
    R0 = D[0,:]
    R=D[1:D.shape[0],:]
    rows=R.shape[0]
    cols=R.shape[1]
    k = 1 / np.log2(rows)
    Rmin = np.amin(R, 0)
    Rmax = np.amax(R, 0)
    A = np.ptp(R, 0)
    y = np.ones([rows, cols])
    y1 = R - Rmin
    y2 = Rmax - R
    for j in range(cols):
        if R0[j] == 0 :
            y[:, j]= y1[:, j] / A[j]
            y[:, j]=y[:, j]*75 + 25

        else :
            y[:, j] = y2[:, j] / A[j]
            y[:, j]=y[:, j]*75 + 25

    S =np. sum(y, axis=0)
    Y = np.zeros([rows, cols])
    for i in range(cols):
        Y[:, i] = y[:, i] / S[i]
    lnYij = np.zeros([rows, cols])
    for i in range(rows):
        for j in range(cols):
            if Y[i, j] == 0:
                lnYij[i, j]= 0
            else:
                lnYij[i, j] = np.log2(Y[i, j])
    ej = -k * (np.sum(Y* lnYij, axis=0))
    s=Y*lnYij
    weights = (1 - ej) / (cols - np.sum(ej));
    F = np.dot(y,weights);
    return [weights,F,y]
if __name__ == '__main__':
    df00=pd.read_excel(r'C:\Users\Eleven最沉着\Desktop\venv\服务业数据.xls')
    D=df00.iloc[0:18,3:17].values.T

    [weights,F,y]=shangquanfa(D)


