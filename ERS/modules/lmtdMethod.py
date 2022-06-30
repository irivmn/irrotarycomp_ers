from cmath import log
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
import numpy as np

def lmtdmethod (T_C_OUT=60, T_C_IN=40, T_H_IN=90, T_H_OUT=60):
    P = (T_C_OUT-T_C_IN)/(T_H_IN-T_C_IN)  
    R = (T_H_IN-T_H_OUT)/(T_C_OUT-T_C_IN)  
    DT_1 = T_H_IN - T_C_OUT  
    DT_2 = T_H_OUT - T_C_IN  
    LMTD = ((DT_1 - DT_2) / log(DT_1 / DT_2)).real
    P=0.3
    R_List = [0.2, 0.4, 0.6, 0.8, 1, 2, 3, 4]
    LMTD_F = [-(4.070*P**3)+(4.645*P**2)-(1.025*P)+1.001,
              -(2.003*P**3)+(1.897*P**2)-(0.407*P)+1.002,
              -(1.660*P**3)+(1.277*P**2)-(0.261*P)+1.002,
              -(1.283*P**3)+(0.583*P**2)-(0.080*P)+1.001,
              -(1.611*P**3)+(0.590*P**2)-(0.061*P)+1.000,
              -(13.493*P**3)+(5.763*P**2)-(0.616*P)+1.004,
              -(47.436*P**3)+(15.322*P**2)-(1.253*P)+1.006, 
              -(182.697*P**3)+(47.418*P**2)-(2.278*P)+1.002]
    R_F = interpolate.splrep(R_List,LMTD_F)
    F=interpolate.splev(R,R_F)
    
    print("P : ",P)
    print("R : ",R)
    print("LMTD_F : ",LMTD_F)
    print("LMTD : ",LMTD)
    print("F : ",F)

    R1 = np.array(R_List)
    L1 = np.array(LMTD_F)

    for order in range(1, 4):
        D = InterpolatedUnivariateSpline(R1, L1, k=order)
        print("LMTD_F : ",D(R))

'''    if R < 4:  
        F=lmtd_cf('crossflow_both_unmixed',P,R)
    else:
        F=0.8
    return (LMTD, F)'''
lmtdmethod()

