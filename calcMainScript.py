# -*- coding: cp936 -*-
#calcMainScript.py

#     1.   initialize

def initialize(L, dx,p_gasIn,p_gasOut):
    m = int(L/dx)
    
    #heliumT
    heliumT= [4.5]*m
    heliumT[int(m/2)]= 20

    #heliumP
    heliumP = [p_gasIn]*m
    dp = (p_gasOut - p_gasIn)/m
    for i in range(m):
        heliumP[i] += dp*i


    #helium density
    heliumDst = [0]*m
    for i in range(m):                        #search the HEPAK excel-file get density from P&T
        xls.setCell(1,9,3,heliumP[i])
        xls.setCell(1,9,4,heliumT[i])
        heliumDst[i] = xls.getCell(1,20,4)
    #helium speed
    for i in range(m):
        spd[i] = 18*0.001/((17.6*11*0.3)*heliumDst[i])

    #coilT
    coilT = heliumT

    #shellT
    shellT = [5.5]*m

    return heliumT, heliumP, heliumDst, coilT, shellT

print initialize(200,0.1,0.30,0.52)
    
#-------------------------------------------------------------------------
#   2. using clacCoilAndShell.py get new temperature-Mat and Source-Term
#   recycle dt/ddt times
def doCalcSolid():
    dt = 1
    ddt = 0.5
    St1Sum = [0]*m
    St2Sum = [0]*m
    mCu = dx*80*pi*0.16*10**(-6)*8900
    mSc = dx*160*pi*0.16*10**(-6)*9140
    mShell = dx*(2.2*(10+17)*10*(-6))*7916/3
    
    for i in range(dt/ddt):
        # coil get temperature-rise from InnerHeat
        coilT = calcCoilAndShell.calcCoilT_InnerHeat(coilT, m , time, dx, ddt , mCu, mSc)
        
        # coil get temperature-change from conductivity between all dx-coil
        coilT = calcCoilAndShell.calcNextCoilT(coilT,m,dx, ddt, mCu, mSc)
        print "coil   自身导热传播"
        print coilT
        # coil get temperature-decrease from cold helium
        dh = 4*((0.3*17.6*10.6*10**6)/(pi*0.8*0.001*240))
        xls.setCell(1,9,3,heliumP[i])
        xls.setCell(1,9,4,heliumT[i])                  
        dynVis = xls.getCell(1,42,4)
        con = xls.getCell(1,43,4)
        Cp = xls.getCell(1,31,4)
        hCoil = calcCoilAndShell.calc_hCoil(heilumDst[i],spd[i],dh,dynVis,Cp,con)
        coilT, StOne = calcCoilAndShell.calcConvectionWithCoil(coilT, heliumT , m,dx, ddt, mCu , mSc, hCoil)
        print "coil 和氦气热交换之后"
        print coilT
        # shell get temperature-change from hot helium
        shellT, StTwo = calcCoilAndShell.calcShellT(shellT,  heliumT ,m, dx,dt ,mShell)
        for j in range(m):
            St1Sum[i] += StOne[i]
            St2Sum[i] += StTwo[i]
        return coilT,shellT, St1Sum, St2Sum

#---------------------------------------------------------------------------------------
#  3 . using calcHelium.py  get new temperature-array of heliumT
#  because of the limit in using xls , we need transfer the part of helium-calculation here
def doCalcHelium():
    nextT = [0]*m
    nextP = [0]*m
    nextDensity = [0]*m
    nextSpd = [0]*m
    
    for i in range(m-2):
        i=i+1
        xls.setCell(1,9,3,heliumP[i])
        xls.setCell(1,9,4,heliumT[i])                  
        dynVis = xls.getCell(1,42,4)
        con = xls.getCell(1,43,4)
        Cp = xls.getCell(1,31,4)
        St = (St1Sum[i]+St2Sum[i])//((17.6*10.6*0.3)*10**(-6))
                           
        nextT[i],nextDensity[i],nextSpd[i]=calcHelium.calcHelium(heliumT[i-1],heliumT[i],heliumT[i+1],
                                                                 heliumP[i],
                                                                 heliumDst[i-1],heliumDst[i],heliumDst[i+1],
                                                                 spd[i-1],spd[i],spd[i+1],
                                                                 dynVis,con,Cp,St)
        
                           
    #deal with the begin_point and end_point
    xls.setCell(1,9,3,heliumP[0])
    xls.setCell(1,9,4,heliumT[0])                  
    dynVis = xls.getCell(1,42,4)
    con = xls.getCell(1,43,4)
    Cp = xls.getCell(1,31,4)
    St = (St1Sum[0]+St2Sum[0])/((17.6*10.6*0.3)*10**(-6))
    nextT[0],nextDensity[0],nextSpd[0]=calcHelium.calcHeliumBeginPoint(0,heliumT[0],heliumT[1],
                                                                 heliumP[0],
                                                                 0,heliumDst[0],heliumDst[1],
                                                                 0,0,spd[1],
                                                                 dynVis,con,Cp,St)
    nextSpd[0]=0
    xls.setCell(1,9,3,heliumP[0])
    xls.setCell(1,9,4,heliumT[0])                  
    dynVis = xls.getCell(1,42,4)
    con = xls.getCell(1,43,4)
    Cp = xls.getCell(1,31,4)
    St = (St1Sum[0]+St2Sum[0])/((17.6*10.6*0.3)*10**(-6))
    nextT[m-1],nextDensity[m-1],nextSpd[m-1]=calcHelium.calcHeliumEndPoint(heliumT[m-2],heliumT[m-1],0,
                                                                 heliumP[m-1],
                                                                 heliumDst[m-2],heliumDst[m-1],0,
                                                                 spd[m-2],spd[m-1],0,
                                                                 dynVis,con,Cp,St)
    nextSpd[m-1]=0

    #get nextP from temperature and density
    xls.setCell(1,7,3,3)
    for i in range(m):
        xls.setCell(1,9,3,nextDensity[i])
        xls.setCell(1,9,4,nextT[i])
        nextP[i] = xls.getCell(1,18,4)
    xls.setCell(1,7,3,1)

    heliumT = nextT
    heliumP = nextP
    heliumDst = nextDensity
    spd = nextSpd
    return heliumT, heliumP, heliumDst, spd
    

    
    



























