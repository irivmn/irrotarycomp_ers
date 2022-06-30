from scipy.interpolate import interp1d
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def ultracoolantprop (I) :
    #read Excel file to import data to dataframe df
    df = pd.read_excel(r'C:\\Users\\pxc2007.ext\\OneDrive - Ingersoll Rand\Documents\\Pavan_Project\\Ultracoolant.xls')
    #print (df)
    #print(list(df["Density"]))

    T = list(df["T"])[1:]
    
    D = interpolate.splrep(T,list(df["Density"])[1:])
    Cp = interpolate.splrep(T,list(df["C_P"])[1:])
    VK = interpolate.splrep(T,list(df["Viscosity_Kinematic"])[1:])
    VD = interpolate.splrep(T,list(df["Viscosity_Dynamic"])[1:])
    Co = interpolate.splrep(T,list(df["Conductivity"])[1:])

    Rho_O = round(float(interpolate.splev(I,D)),3)
    C_p_O = round(float(interpolate.splev(I,Cp)),3)
    Mu_O  = round(float(interpolate.splev(I,VD)),4)
    k_O   = round(float(interpolate.splev(I,Co)),6)
    Pr_O = (Mu_O*C_p_O)/k_O

    return (Rho_O,C_p_O,Mu_O,k_O,Pr_O)
    
