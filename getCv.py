# -*- coding: cp936 -*-
import urllib2,urllib
import oneVariableCubicEquation
from numpy import *

'''
#计算线圈内气体的比体积
def calv0(pressure,temp):
    a = 0.0324*10**6
    b = 23.4
    R = 8.31451
    s1 = pressure
    s2 = -(pressure*b+R*temp)
    s3 = a
    s4 = -a*b
    ans = oneVariableCubicEquation.getCubicRoot(s1,s2,s3,s4)
    return ans
print calv0(0.41,4.2)
    
'''

'''



v = 33.336  # cm3/mol
#通过状态方程以及温度 T ， 计算压强 p
def pressure(temp,v):
    R = 83.1451
    a = -0.0005808
    A0 = 0.0414945
    b = -0.00000019727
    B0 = 0.023661
    C = -0.005592
    alpha = -0.0000072673
    C0 = -0.00000164379
    gama = 0.00077942

    p1 = R*temp/v + (B0*R*temp-A0-C0/(temp**2))/(v**2)
    p2 = (b*R*temp-a)/(v**3) + a*alpha/(v**6)
    p3 = (C*(1+gama/(v**2))*exp(-alpha/(v**2)))/((temp**2)*(v**3))
    p = p1 + p2 + p3
    
    return p

print pressure(5.2,v)  














'''
#从网上获得氦气的定压比热容
#temp = 34.5
#pressure = 0.3

'''
def getCv(temp, pressure):
    #从http://webbook.nist.gov获得地址
    heliumurl = "http://webbook.nist.gov/cgi/fluid.cgi?Action=Load&ID=C7440597&Type=IsoTherm&Digits=5&PLow="+str(pressure)+"&PHigh="+str(pressure)+"&PInc=0&T="+str(temp)+"&RefState=DEF&TUnit=K&PUnit=MPa&DUnit=mol%2Fl&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm"
    #heliumdlurl = "http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID=C7440597&Type=IsoTherm&Digits=5&PLow="+str(pressure)+"&PHigh="+str(pressure)+"&PInc=0&T="+str(temp)+"&RefState=DEF&TUnit=K&PUnit=MPa&DUnit=mol%2Fl&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm"
    url = heliumurl
    up = urllib2.urlopen(url)
    cont = up.read()
    #print cont
    head = '<td align="right">'
    rd = 0
    ph = 0
    while(rd<8):
        ph = cont.find(head,ph+10,len(cont))
        rd = rd+1
        #print rd,ph
    Cv = cont[ph+len(head):ph+len(head)+6]
    return Cv

#print getCv(temp,pressure)

''' 

def getVandCv(temp,pressure):
    #从http://webbook.nist.gov获得地址
    heliumurl = "http://webbook.nist.gov/cgi/fluid.cgi?Action=Load&ID=C7440597&Type=IsoTherm&Digits=5&PLow="+str(pressure)+"&PHigh="+str(pressure)+"&PInc=0&T="+str(temp)+"&RefState=DEF&TUnit=K&PUnit=MPa&DUnit=mol%2Fl&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm"
    #heliumdlurl = "http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID=C7440597&Type=IsoTherm&Digits=5&PLow="+str(pressure)+"&PHigh="+str(pressure)+"&PInc=0&T="+str(temp)+"&RefState=DEF&TUnit=K&PUnit=MPa&DUnit=mol%2Fl&HUnit=kJ%2Fmol&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm"
    url = heliumurl
    up = urllib2.urlopen(url)
    cont = up.read()
    #print cont
    head = '<td align="right">'
    rd = 0
    vh = 0
    ph = 0
    while(rd<4):
        vh = cont.find(head,vh+10,len(cont))
        rd = rd +1
    ph = vh
    while(rd<8):
        ph = cont.find(head,ph+10,len(cont))
        rd = rd+1
        #print rd,ph
    v = float(cont[vh+len(head):vh+len(head)+6])
    Cv = float(cont[ph+len(head):ph+len(head)+6])
    return v,Cv

#test part
print 'temp    ','pressure      ','v    ','         Cv'
attempts = 0
for i in range(100):
    for j in range(10):
        temp = 4.5+i*0.1
        pressure = 0.30+j*0.01
        #print temp , pressure
        try:
            v,Cv = getVandCv(temp,pressure)
            success = True
        except:
            attempts +=1
            if attempts == 10:
                print temp, '   ',pressure,'   output wrong'
        print temp,'         ',pressure,'        ',v,'     ',Cv

        
'''


# 筛选比体积v=  时的 p 和 T 的值
T0 = 4.5     #起点
p0 = 0.41
v0,Cv0 = getVandCv(T0,p0)   

def choosePandCv(T1,T0,p0):
    #v,Cv = getVandCv(T1,p0)
    try:
        v,Cv = getVandCv(T1,p0)
        success = True
    except:
        attempts +=1
        if attempts == 10:
            print temp,'   ',pressure,'   output wrong'
    p = p0
    #print v,v0
    #print Cv,Cv0
    while(v>v0):
        vhigh = v
        Cvhigh = Cv
        pbegin = p
        p=p+0.01
        v,Cv = getVandCv(T1,p)
        #print v,Cv
    vlow = v
    Cvlow = Cv
    pend = p
    ratelow = (vhigh-v0)/((vhigh-v0) + (v0-vlow))
    ratehigh = (v0-vlow)/((vhigh-v0) + (v0-vlow))
    #print ratelow+ratehigh
    p1 = pbegin*ratehigh + pend*ratelow
    Cv1 = Cvhigh*ratehigh+Cvlow*ratelow
    v1 = vhigh*ratehigh+vlow*ratelow
    return p1,v1,Cv1

#print choosePandCv(4.6,4.5,0.41)
'''

'''
for i in range(50):
    T1= T0 + 0.1
    p1,v1,Cv1 = choosePandCv(T1,T0,p0)
    print T1,p1,v1,Cv1
    T0 = T1
    p0 = p1

'''








