# -*- coding: cp936 -*-
#filename calcHelium.py
from numpy import *

#using Hepak get data needed
    #density = calcDensity(T,P)  #?????????????????????????????????可以在clacMainUsingExcel.py中解决

#------------------------------------------------------------------------------------------------------------------------------------------------
#function: calculation value of the time(n+1) ,data-input is of time(n)
def calcHeliumGeneral(dt,dx,T0, T1, T2, P0, P1,P2, density0, density1, density2, spd0, spd1, spd2, dynVis,con,Cp,St):
    # Continous formula
    num1=density2*spd2 - density0*spd0
    nextDensity1=density1-(0.5*dt/dx)*num1

    #  N-S formula
    #dynVis = clacDynViscosity(T1, P1)   # clac the DYNAMIC VISCOSITY of time(n)  ??????????????????????????
    #con = clacThermalConductivity(T1, P1)       # clac the THERMAL CONDUCTIVITY  of time(n)  ??????????????????????????
    SuNum1 = (spd2-2*spd1+spd0)/(dx**2)
    Su = (dynVis + con )*SuNum1
    Su=0  #########################
    spdNum1 = (0.5*dt/dx)*(density2*(spd2*abs(spd2)) - density0*(spd0*abs(spd0)))
    spdNum2 = (dynVis*dt/dx**2)*(spd2-2*spd1+spd0)
    spdNum3 = Su*dt - (0.5*dt/dx)*(P2-P0)
    nextSpd1 = (density1*spd1 - spdNum1 + spdNum2 + spdNum3)/nextDensity1

    # Energy formula
    #Cp = calcCp(T1, P1)                      #calc the SPECIAL HEAT CAPACITY of time(n)  ??????????????????????????
    #St = calcSourceTerm(-------------)              #calc the SOURCE TERM of time(n)   ???????????????????????????????????????
    tempNum1 = (density1*spd1)/nextDensity1
    tempNum2 = dt*(density2*spd2*T2 - density0*spd0*T0)/(nextDensity1*2*dx)
    tempNum3 = dt*(- (P1*spd2-P1*spd0)/(2*dx) + con*(T2-2*T1+T0)/(dx**2) + St)
    nextT1 = tempNum1 - tempNum2 + tempNum3/(Cp*nextDensity1)

    # clac PRESURRE of time(n+1)
    #nextP1 = clacPressure(nextT1, nextDensity1)    #??????????????????????????????????????

    return nextT1, nextDensity1, nextSpd1
# clac PRESURRE of time(n+1)
    #nextP1 = clacPressure(nextT1, nextDensity1)    #??????????????????????????????????????  get nextP1

def calcHeliumBeginPoint(dt,dx,T0, T1, T2, P0, P1,P2, density0, density1, density2, spd0, spd1, spd2, dynVis,con,Cp,St):
    # Continous formula
    num1=density2*spd2 - density1*spd1
    nextDensity1=density1-(dt/dx)*num1

    #  N-S formula
    #dynVis = clacDynViscosity(T1, P1)   # clac the DYNAMIC VISCOSITY of time(n)  ??????????????????????????
    #con = clacThermalConductivity(T1, P1)       # clac the THERMAL CONDUCTIVITY  of time(n)  ??????????????????????????
    SuNum1 = (spd2-spd1)/(dx**2)
    Su = (dynVis + con )*SuNum1
    Su=0  #########################

    spdNum1 = (dt/dx)*(density2*(spd2*abs(spd2)) - density1*(spd1*abs(spd1)))
    spdNum2 = (dynVis*dt/dx**2)*(spd2-spd1)
    spdNum3 = Su*dt - (dt/dx)*(P2-P1)
    nextSpd1 = (density1*spd1 - spdNum1 + spdNum2 + spdNum3)/nextDensity1

    # Energy formula
    #Cp = calcCp(T1, P1)                      #calc the SPECIAL HEAT CAPACITY of time(n)  ??????????????????????????
    #St = calcSourceTerm(-------------)              #calc the SOURCE TERM of time(n)   ???????????????????????????????????????
    tempNum1 = (density1*spd1)/nextDensity1
    tempNum2 = dt*(density2*spd2*T2 - density1*spd1*T1)/(nextDensity1*dx)
    tempNum3 = dt*( - (P1*spd2-P1*spd1)/(dx) + con*(T2-T1)/(dx**2) + St)
    nextT1 = tempNum1 - tempNum2 + tempNum3/(Cp*nextDensity1)

    # clac PRESURRE of time(n+1)
    #nextP1 = clacPressure(nextT1, nextDensity1)    #??????????????????????????????????????

    return nextT1, nextDensity1, nextSpd1

def calcHeliumEndPoint(dt,dx,T0, T1, T2, P0, P1, P2,density0, density1, density2, spd0, spd1, spd2, dynVis,con,Cp,St):
    # Continous formula
    num1=density0*spd0 - density1*spd1
    nextDensity1=density1-(dt/dx)*num1

    #  N-S formula
    #dynVis = clacDynViscosity(T1, P1)   # clac the DYNAMIC VISCOSITY of time(n)  ??????????????????????????
    #con = clacThermalConductivity(T1, P1)       # clac the THERMAL CONDUCTIVITY  of time(n)  ??????????????????????????
    SuNum1 = (spd1-spd0)/(dx**2)
    Su = (dynVis + con )*SuNum1
    Su=0  #########################
    spdNum1 = (dt/dx)*(density1*(spd1*abs(spd1)) - density0*(spd0*abs(spd0)))
    spdNum2 = (dynVis*dt/dx**2)*(spd1-spd0)
    spdNum3 = Su*dt - (dt/dx)*(P1-P0)
    nextSpd1 = (density1*spd1 - spdNum1 + spdNum2 + spdNum3)/nextDensity1

    # Energy formula
    #Cp = calcCp(T1, P1)                      #calc the SPECIAL HEAT CAPACITY of time(n)  ??????????????????????????
    #St = calcSourceTerm(-------------)              #calc the SOURCE TERM of time(n)   ???????????????????????????????????????
    tempNum1 = (density1*spd1)/nextDensity1
    tempNum2 = dt*(density1*spd1*T1 - density0*spd0*T0)/(nextDensity1*dx)
    tempNum3 = dt*(- (P1*spd1-P1*spd0)/(dx) + con*(T1-T0)/(dx**2) + St)
    nextT1 = tempNum1 - tempNum2 + tempNum3/(Cp*nextDensity1)

    # clac PRESURRE of time(n+1)
    #nextP1 = clacPressure(nextT1, nextDensity1)    #??????????????????????????????????????

    return nextT1, nextDensity1, nextSpd1







'''

#-------------------------------------------------------------------------------------------------------------------------------------------
def SourceTerm()


#--------------------------------------------------------------------------
#线圈是在dt时间内，分一百步进行整个线圈上的迭代计算，每一步先计算线圈部分的导热，再计算导热后
#的线圈与氦气之间的换热，从而更新一下线圈的温度，再进行下一步的计算
def clacCoil(float coilT[]):      
    #Implicit Format
    m=len(coilT)
    coilMat = zeros((m,m))
    for i in range(len(coilT)):
                                                                        这部分已经在coilTandShell.py中完成
 '''       
              



        
        
    






























    
    
    

    
    #continous formula
    #function: calculation of the time(n+1) on density
    
    

