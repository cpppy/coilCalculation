# -*- coding: cp936 -*-
from numpy import *
import getCv

T0 = 4.5     #起点
p0 = 0.41
v0,Cv0 = getCv.getVandCv(T0,p0) 

Va = 17.6*10.6*314.5*0.3*10**(-6)
Vbc = 15.8*9*(368.05+208.5+213.58+219.11+224.64)*0.3*10**(-6)
Vd = 11*10.4*273.48*12*0.3*10**(-6)
Vhelium = Va + Vbc +Vd
mhelium = Vhelium/v0
print Vhelium,mhelium
'''
Q = 0
T1 = T0
Cv1 = Cv0
print 'T1   p1          Q'
while(Q<2800):
    T1 = T1+0.1
    Q = Q + mhelium*Cv1*0.1
    p1,v1,Cv1 = getCv.choosePandCv(T1,T0,p0)
    print T1,p1,Q
    T0 = T1
    p0 = p1

print 'the calculation has been finished'
print  'T =  ',T0
print 'P = ',p0
'''    
    
    



















    
