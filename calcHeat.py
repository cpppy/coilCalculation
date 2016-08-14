# -*- coding: cp936 -*-
from numpy import *
import math

def electricCurrent(time):
    I0 = 14000
    Rd =  0.286
    L = 1.02975
    I = I0*exp(-Rd*time/L)
    return I


def dIdt(time):
    I0 = 14000  
    R =  0.286
    L = 1.02975
    dIdt = (I0*exp(-R*time/L))*(-R/L)
    return dIdt

def Bvalue(time):
    I0 = 14000
    Rd =  0.286
    L = 1.02975
    I = I0*exp(-Rd*time/L)
    u0 = 4*pi*10**(-7)
    B = 0.5*u0*I*(104/0.482 + 114/0.514 + 228/0.604 +720/0.7255)
    return B
    
def dmagneticFieldStrenth(dIdt):    #计算磁场强度变化率（随时间）
    u0 = 4*pi*10**(-7)
    dBdt = 0.5*u0*dIdt*(104/0.482 + 114/0.514 + 228/0.604 +720/0.7255)
    return dBdt



    





















    
    
