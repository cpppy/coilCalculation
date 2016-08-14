#calcInnerHeat.py
# -*- coding: cp936 -*-
#get dQinner from the input value time
import calcHeat
import getPhysicalParameters
from numpy import *
import math

def get_innerHeat(time,T ,dx,ddt):
    dIdt = abs(calcHeat.dIdt(time))
    dBdt = calcHeat.dmagneticFieldStrenth(dIdt)
    #磁滞损耗计算
    B = calcHeat.Bvalue(time)
    '''
    if(T>=17):
        Jc, Tc = calcJcTc(T,B/4)
    else:
    '''
    Jc = 1000*10000      #此处应寻找表达式来算
    deff = 0.8*10**(-3)
    AscMultiLen = dx*pi*0.16*10**(-6)*160  #此处应修改为dx段的数值 A线圈160根超导细丝.80.42contain 160
    dQh = (2*Jc*deff*AscMultiLen*dBdt/(3*pi))*ddt
    
    #耦合损耗计算
    nt = 0.1  #耦合时间常数 预设为 0.1S
    u0 = 4*pi*10**(-7)
    Vsc = AscMultiLen
    dQc = (Vsc*nt*(dBdt**2)/u0)*ddt

    #焦耳热的计算
    
    if(T>=6):
        I = calcHeat.electricCurrent(time)   #四根中失超线圈的电流？？？？？？？阻值不同时的电流分配
        #troublelen = 400   #参数未知(失超长度)
        #temp =  220    #参数未知（失超温度）
        B = calcHeat.Bvalue(time)  
        '''
        #R = troublelen*r/Acu
        s = pi*0.16*10**(-6) #单根铜细丝的截面积
        Ra = r*416.9/(80*s)  #线圈A中铜的电阻
        Rb = r*487.6/(75*s)
        Rc = r*1143.3/(120*s)
        Rd = r*4350/(180*s)
        R = 1/((1/Ra)+(1/Rb)+(1/Rc)+(1/Rd))
        '''
        r = getPhysicalParameters.get_rCu(T,B)
        #print "r= ",r
        s = pi*0.16*10**(-6) #单根铜细丝的截面积
        Ra = r*dx/(80*s)  #线圈A中铜的电阻
        dJheat = ((I/4)**2)*Ra*ddt   #假设电流在四个线圈上平均分配
        #print "dJheat = ",dJheat,"-------------------------------------------"
    else:
        dJheat = 0

    dQinner = dJheat+dQh+dQc
    #print  "dQinner = ",dQinner
    return dQinner

def calcJcTc(T,B):
    #B=B/4
    a=900
    BC20m = 28
    TCOM = 18
    BC20=BC20m*(1-a*0.0025**1.7)
    TC0 = TCOM*(1-a*0.0025**1.7)**0.333333
    tt = T/TC0
    BC2 = BC20*(1-tt**2)*(1-0.31*tt*(1-1.77*math.log10(tt)))
    bb = B/BC2
    
    C0=1.07*10**10
    C=C0*(1-a*0.0025**1.7)**0.5
    
    TC=TC0
    JC1 = C*(BC2**(-0.5))*(1-tt**2)**2
    JC2 = (bb**(-0.5))*(1-bb)**2
    JC=JC1*JC2
    return JC,TC
    
#print calcJcTc(17,10)








    
