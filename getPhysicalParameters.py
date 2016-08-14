# -*- coding: cp936 -*-
#getPhysicalParameters.py
'''
function get the Thermal Conductivity and Thermal Capacity
    of   Cu \ Nb3Sn \ LN316  of Line \ Shell
'''
from numpy import *
import math
import calcHeat
import calcInnerHeat

def formula(a,b,c,d,e,f,g,h,i,T):
    num1=math.log10(T)
    num2=a+b*num1+c*(num1**2)+d*(num1**3)
    num3=e*(num1**4)+f*(num1**5)
    num4=g*(num1**6)+h*(num1**7)+i*(num1**8)
    num5=num2+num3+num4
    return 10**num5

# calculaition of thermal capacity
def get_cCu(T):
    num1=math.log10(T)
    num2=(-1.91844)+(-0.15973)*num1+8.61013*(num1**2)+(-18.996)*(num1**3)
    num3=(21.9661)*(num1**4)+(-12.7328)*(num1**5)
    num4=(3.54322)*(num1**6)+(-0.3797)*(num1**7)
    num5=num2+num3+num4
    return 10**num5
'''
for i in range(20):
    print "T=",10+10*i,"   ",get_cCu(10+10*i)
'''

def get_cShell(T):   #shell material： 316LN  不对 需要按照 gandolf修改
    if(T>4 and T<50):
        num1=math.log10(T)
        num2=(12.2486)+(-80.6422)*num1+218.743*(num1**2)+(-308.854)*(num1**3)
        num3=(239.5296)*(num1**4)+(-89.9982)*(num1**5)
        num4=(3.15315)*(num1**6)+(8.44996)*(num1**7)+(-1.91368)*(num1**8)
        num5=num2+num3+num4
        return 10**num5
    else:
        a=-1879.46
        b=3643.19
        c=76.7012
        d=-6176.02
        e=7437.624
        f=-4305.721
        g=1382.462
        h=-237.227
        i=17.052
        return formula(a,b,c,d,e,f,g,h,i,T)
    '''
for i in range(20):
    print "T=",100+10*i,"   ",get_cShell(10+10*i)
   '''

def get_cNb3Sn(T):                 #没有写完整？？？？？？？？？？？？？？？？？？
    AA = 38.2226877
    BB=848.364226
    CC =1415.13808
    DD =-346.837966
    a  =6.80458608
    b =59.9209182
    c= 25.8286334
    d =  8.77918335
    na = 1
    nb =2
    nc= 3
    nd =4
    TMIN =20.0
    TMAX = 1000.0
    #B = calcHeat.Bvalue(time)
    #JC,TC=calcInnerHeat.calcJcTc(T,B)
    TC = 17
    TCS=7.8
    TC0=TC
    if(T<10):
        CPN = (7.5475E-3)*T**2
    elif (T>=10 and T<=20):
        CPN=(-0.3 + 0.00375*T**2)/(0.09937)
    else:
        TT=T
        TT=min(TT,TMAX)
        CPN = AA*TT   /(a+TT)**na + BB*TT**2/(b+TT)**nb + CC*TT**3/(c+TT)**nc + DD*TT**4/(d+TT)**nd
    if (T<TC):
        TT=TC/TC0
        DBC2DT=(-0.46306) - (0.067830)*TC
        DELCP=1500.0*(DBC2DT**2)/(2.0*(27.2/(1.0+(0.34*TT)))**2-1.0)
        if(TC<10):
            CPNTC=(7.5475E-3)*TC**2
        elif(TC>=10 and TC<20):
            CPNTC=(-0.3+0.00375*TC**2)/(0.09937)
        CPS=(CPNTC+DELCP)*(T/TC)**3
    else:
        CPS=0
    if(T<TCS):
        CP=CPS
    elif(T>=TCS and T<=TC):
        if(TCS<TC):
            F= (T-TCS)/(TC-TCS)
        else:
            F=1.0
        CP=F*CPN + (1.0-F)*CPS
    elif(T>TC):
        CP= CPN
    CPNBSN = CP
    return CPNBSN


#calculation of thermal conductivity
def get_conShell(T):                               #316LN
    a=-1.4087
    b=1.3982
    c=0.2543
    d=-0.6260
    e=0.2334
    f=0.4256
    g=-0.4658
    h=0.1650
    i=-0.0199
    return formula(a,b,c,d,e,f,g,h,i,T)


def get_conCu(T):     #from gandalf/solids.f   Cu
    RRR=1000      #?????????????????????????????????????????????????????
    TCU =40.0
    RC0=15.53/(RRR-1.0)
    COND=1.0/(RC0/24.45/T + (33.5E-08)*T*T )
    if(T>TCU):
        COND = COND + 400.*(1.-exp(-(T-TCU)/TCU))
    else:
        COND = 0
    return COND





def get_conNb3Sn(T):      #from gandalf/solids.f  4K---750K   Nb3Sn
    if(T>750):
        T=750
    T0=21.9620369
    A=1.3905E+14
    B=76.6127237
    n=3.66343961
    m=9.3220843
    C=-0.71614565
    D=5.40229689
    if(T<=T0):
        CONBSN = A*T**n/(B+T)**m
    else:
        CONBSN = C*math.log10(T)+D
    return CONBSN


# calc the Electrical resistivity of Copper in Ohm m
def get_rCu(T,B):                       # temperature and magnetic field    from gandalf
    RRR=1000   #?????????????????????????????????????????????????????????????????
    C=[[0.0000 , 0.0082 ,   0.2213 ],
       [ 0.9820 , 2.1741 ,   3.5551 ],
       [ 4.9915 ,   6.4292 ,  7.8496  ],
       [ 9.2483 ,  10.6260 ,  11.9850  ],
       [  13.3279 ,  14.6571 ,  15.9747  ],
       [ 17.2826 ,  18.5821 ,  19.8745  ],
       [   21.1608 ,  22.4419 ,23.7183],
       [ 24.9908 ,  26.2599 ,  27.5259  ],
       [   0.0000 ,   0.0100 ,   0.4782  ],
       [   1.0459 ,1.3303 ,   1.4273 ],
       [  1.4438 ,   1.4308 , 1.4096],
       [  1.3874 ,   1.3678 ,   1.3503  ],
       [  1.3356 ,   1.3228 ,   1.3124  ],
       [ 1.3032 , 1.2959 ,   1.2892 ],
       [  1.2832 ,   1.2785 , 1.2746 ],
       [   1.2709 ,   1.2676 ,   1.2643   ],
       [  0.0082 ,   0.2031 ,   0.2825 ],
       [  0.1462 , 0.0507 ,   0.0091],
       [ -0.0061 ,  -0.0104 ,  -0.0109],
       [ -0.0097 ,  -0.0088 ,  -0.0074  ],
       [  -0.0064 ,  -0.0052 ,  -0.0045 ],
       [ -0.0037 ,-0.0035 ,  -0.0029   ],
       [  -0.0021 ,  -0.0021 , -0.0021],
       [-0.0018 ,  -0.0016 ,  -0.0011]]
    TT= 0.05*T
    IT= int(TT)
    IT= min(IT,23)
    DT= TT-IT
    IT= IT+1
    RC0= 15.53 / (RRR-1.0)
    RHO= (1.0E-9) * (RC0+C[IT-1][0] + DT * (C[IT-1][1] + DT * C[IT-1][2]))
    X=(1.55E-7)*B/RHO
    RHO=RHO*(1.0+(3.046E-4)*X-(6.13E-10)*X*X)
    return RHO


def RofCu(temp):            #from paper
    RRR = 100
    P1 = 1.171*10**(-17)
    P2 = 4.49
    P3 = 3.841*10**10
    P4 = -1.14
    P5 = 50
    P6 = 6.428
    P7 = 0.4531

    roo = 1.553*10**(-8)/RRR
    roi1 = P1*temp**P2
    roi2 = P1*P3*temp**(P2+P4)
    roi3 = roi2    #*exp((P5/temp)**6)
    roi = (roi1)/(1+roi3)
    roio = P7*roi*roo/(roi + roo)

    r = roo + roi + roio
    return r




num1=1-900*(0.0025**1.7)
num2 = 18*num1**0.33333
#print "TC0 = ",num2























