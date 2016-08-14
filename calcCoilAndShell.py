# -*- coding: cp936 -*-
#filename clacCoilAndShell.py
from numpy import *
import getPhysicalParameters
import calcInnerHeat

#通过calcInnerHeat.py计算自发热导致的线圈升温情况
def calcCoilT_InnerHeat(coilT, m, time, dx, ddt , mCu, mSc):
    for i in range(m):
        dQinner = calcInnerHeat.get_innerHeat(time, coilT[i] , dx, ddt)
        cCu = getPhysicalParameters.get_cCu(coilT[i])
        #print "cCu = ", cCu
        cSc = getPhysicalParameters.get_cNb3Sn(coilT[i])
        #print "cSc = ", cSc
        coilT[i] = coilT[i]+dQinner/(mCu*cCu+mSc*cSc)
        #print "coilT[%d] = "%(i),coilT[i]
    return coilT


#--------------------------------------------------------------------------
#线圈是在dt时间内，分一百步进行整个线圈上的迭代计算，每一步先计算线圈部分的导热，再计算导热后
#的线圈与氦气之间的换热，从而更新一下线圈的温度，再进行下一步的计算
#目标二是得到源项的第一部分，即先线圈传递给流体的热量（可正可负）
def calcNextCoilT(coilT,m,dx, ddt, mCu, mSc):   #输入 coilT的列向量 可用coilT.transpose()进行转置
    #Implicit Format of Conductive Heat Transfer
    '''
    #构建隐式格式的系数矩阵coilMat
    coilMat = [[0 for col in range(m)] for row in range(m)]
    #the first row
    coilMat[0][0]  = calcA(coilT[0], m, dx , ddt, mCu, mSc) + 1   #calcA()
    coilMat[0][1]  = -1
    coilT[0] *= calcA(coilT[0], m, dx , ddt, mCu, mSc)
    #the last row
    coilMat[m-1][m-1]  = calcA(coilT[m-1], m, dx , ddt, mCu, mSc) + 1  #calcA() 
    coilMat[m-1][m-2]  = -1
    coilT[m-1] *= calcA(coilT[m-1], m, dx ,ddt, mCu, mSc)
    
    for i in range(m-2):
        coilMat[i+1][i]=-1
        tempA = calcA(coilT[i+1], m, dx , ddt ,mCu, mSc)  #calcA()
        coilMat[i+1][i+1]  =  tempA+2
        coilMat[i+1][i+2]=-1
        coilT[i+1] *= tempA
        
    #对mat取逆后与n时刻的温度场列向量(矩阵形式)点乘
    colCoilT = mat(coilT)
    coilMat = mat(coilMat)
    nextCoilT = (coilMat.I)*colCoilT.T
    for i in range(m):        #将单列的矩阵还原成列表形式
        coilT[i]=float(nextCoilT[i])    
    return  coilT

def calcA(T, m, dx , ddt, mCu, mSc):   #计算线圈导热中用到的a作为系数因子
    AreaCon =  (160+80)*pi*0.16*10**(-6)   # 线圈导热时用到的横截面积
    cCu = getPhysicalParameters.get_cCu(T)
    cSc = getPhysicalParameters.get_cNb3Sn(T)
    conCu = getPhysicalParameters.get_conCu(T)
    conSc = getPhysicalParameters.get_conNb3Sn(T)
    c = (mCu*cCu+mSc*cSc)/(mCu+mSc)
    con = (mCu*conCu+mSc*conSc)/(mCu+mSc)
    A=dx*(mCu+mSc)*c/(con*AreaCon*ddt)
    return A
    '''
    #采用显式格式进行计算
    newCoilT = [0]*m
    AreaCon =  (160+80)*pi*0.16*10**(-6)   # 线圈导热时用到的横截面积
    for i in range(m):
        T =coilT[i]
        cCu = getPhysicalParameters.get_cCu(T)
        cSc = getPhysicalParameters.get_cNb3Sn(T)
        conCu = getPhysicalParameters.get_conCu(T)
        conSc = getPhysicalParameters.get_conNb3Sn(T)
        c = (mCu*cCu+mSc*cSc)/(mCu+mSc)
        con = (mCu*conCu+mSc*conSc)/(mCu+mSc)
        a=ddt*con*AreaCon*(mCu+mSc)*c/dx
        if(i==0):
            newCoilT[i] = coilT[i]+a*(coilT[i+1]-coilT[i])
        elif(i==m-1):
            newCoilT[i] = coilT[i]+a*(coilT[i-1]-coilT[i])
        else:
            newCoilT[i] = coilT[i]+a*(coilT[i+1]-2*coilT[i]+coilT[i-1])
    #coilT = newCoilT
    return newCoilT
                         

#计算ddt = dt/100时间内 线圈与氦气之间的换热
def calcConvectionWithCoil(coilT, heliumT , m,dx, ddt, mCu , mSc, hCoil):
    b=[0]*m
    StOne = [0]*m  # the 1st part of Source Term
    tempQ=0
    newnewCoilT = [0]*m
    Area =  (160+80)*pi*0.8*0.001*dx            #area 是线与氦气之间的换热面积
    for i in range(m):
        cCu = getPhysicalParameters.get_cCu(coilT[i])
        cSc = getPhysicalParameters.get_cNb3Sn(coilT[i])
        c = (mCu*cCu+mSc*cSc)/(mCu+mSc)
        a = ddt*Area*hCoil[i]/(mCu*cCu+mSc*cSc)       
        #newCoilT[i] = (a*heliumT[i]+(1-3*a/8)*coilT[i])/(1+5*a/8)
        #修改为将n时刻的比重降为0
        #print 'c = ',c
        #print 'a = ',a
        newnewCoilT[i] = (a*heliumT[i]+(1-0*a/8)*coilT[i])/(1+8*a/8)
        #print 'helium',heliumT[i],'coil 0 ' ,coilT[i],'coil 1 ' ,newnewCoilT[i]
        StOne[i] = (mCu*cCu+mSc*cSc)*(coilT[i]-newnewCoilT[i])
    #coilT = newnewCoilT
    return newnewCoilT, StOne




#计算 dt 时间内壳体内部温度场的变化 以及 壳体部分与氦气之间的换热
# shellT 是一个m行3列的矩阵
def calcShellT(shellT,  heliumT ,m, dx,dt , mShell):
    #mTe = ????每一个 dx小段的 每一个层的 铁壳的 质量
    Area = (17.6+10.6)*0.001*dx    
    StTwo=[0]*m          # the 2nd part of Source Term
    for i in range(m):
        c1 = Area*con(shellT[i][1])/(mShell*cTe(shellT[i][1])*dx)
        c2 = Area*con(shellT[i][2])/(mShell*cTe(shellT[i][2])*dx)
        c3 = 2*Area*con(shellT[i][3])/(mShell*cTe(shellT[i][2])*dx)
        newT0 = heliumT[0]
        newT1 = shellT[i][1] + c1*(shellT[i][0]-2*shellT[i][1]+shellT[i][2])
        newT2 = shellT[i][2] + c2*(shellT[i][1]-2*shellT[i][2]+shellT[i][3])
        newT3 = shellT[i][3] + c3*(shellT[i][2]-shellT[i][3])
        StTwo[i] =  Area*con(shellT[i][1])*(shellT[i][0]-shellT[i][1])/dx
        shellT[i][0] = newT0
        shellT[i][1] = newT1
        shellT[i][2] = newT2
        shellT[i][3] = newT3
    return shellT, StTwo
    
def con(T):         #计算Shell中各节点处的导热系数con
    return getPhysicalParameters.get_conShell(T)

def cTe(T):         #计算Shell中各节点处的比热容
    return getPhysicalParameters.get_cShell(T)

def calc_hCoil(density,spd,dh,dynVis,Cp,con):   #计算线圈与氦气之间的换热系数公式
    #print "spd = ",spd,'\n'
    spd=abs(spd)
    #print "dh = ",dh,'\n'
    #print "dynVis = ",dynVis,'\n'
    Re = density*spd*dh/dynVis
    Pr = Cp*dynVis/con
    Nu = 0.023*(Re**0.8)*(Pr**0.4)
    hCoil = Nu*con/dh
    #print "Re = ",Re,'\n'
    #print "Pr = ",Pr,'\n'
    #print "Nu = ",Nu,'\n'
    return hCoil




























    
        
        
