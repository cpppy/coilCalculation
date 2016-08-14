# -*- coding: cp936 -*-
import calcHeat
from numpy import *
import matplotlib.pyplot as plt
import pylab as pl

'''
I = calcHeat.electricCurrent(3.61)
print I
'''
ddtime = 0.001
time = 0
Qh = 0
Qc = 0
Jheat = 0
Q = 0
iend = 0

#定义数组用于画图
arrI = [0 for x in range(10000)]
arrB= [0 for x in range(10000)]
arrQh = [0 for x in range(10000)]
arrQc = [0 for x in range(10000)]
arrJheat = [0 for x in range(10000)]
arrQ = [0 for x in range(10000)]
arrtime = [0 for x in range(10000)]

print 'Qh                               Qc                              Jheat'

for i in range(10000):
    dt = ddtime
    #dt = (i)*ddtime   这种做法是使用退火算法加速计算的
    time = time+dt
    print ' i = ',i,'   time = ',time
    arrtime[i] = time
    dIdt = abs(calcHeat.dIdt(time))
    dBdt = calcHeat.dmagneticFieldStrenth(dIdt)
    #磁滞损耗计算
    Jc = 1000*10000      #此处应寻找表达式来算
    deff = 80*10**(-6)
    AscMultiLen = (80.42*416.9+52.78*487.6+30.16*1143.3+18.10*4350)*10**(-6)
    dQh = (2*Jc*deff*AscMultiLen*dBdt/(3*pi))*dt
    Qh = Qh + dQh
    arrQh[i] = Qh
    
    #耦合损耗计算
    nt = 0.1  #耦合时间常数 预设为 0.1S
    u0 = 4*pi*10**(-7)
    Vsc = AscMultiLen
    dQc = (Vsc*nt*(dBdt**2)/u0)*dt
    Qc = Qc+dQc
    arrQc[i] = Qc

    #焦耳热的计算
    I = calcHeat.electricCurrent(time)   #四根线圈的总电流
    arrI[i] = I
    #troublelen = 400   #参数未知(失超长度)
    #temp =  220    #参数未知（失超温度）
    r = 2.1*10**(-9)    #此处用朱加伍的平均值，实际需要公式 r = calcHeat.RofCu(temp) 来确定
    #R = troublelen*r/Acu
    s = pi*0.16*10**(-6) #单根铜细丝的截面积
    Ra = r*416.9/(80*s)  #线圈A中铜的电阻
    Rb = r*487.6/(75*s)
    Rc = r*1143.3/(120*s)
    Rd = r*4350/(180*s)
    R = 1/((1/Ra)+(1/Rb)+(1/Rc)+(1/Rd))
    
    
    dJheat = (I**2)*R*dt
    Jheat = Jheat + dJheat
    arrJheat[i] = Jheat
    
    Qlast = Q
    print Qh,'   ',Qc,'   ',Jheat
    Q = Q+dQh+dQc+dJheat
    print Q
    arrQ[i] = Q
    B = calcHeat.Bvalue(I)
    #print B
    arrB[i] = B

    if Q-Qlast<0.01*Q*dt:
        iend = i
        break
print 'have been static'
print 'time= ',time
print Q
print 'R = ',R


#画图部分
fig = plt.figure()
ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)
ax3 = fig.add_subplot(323)
ax4 = fig.add_subplot(324)
ax5 = fig.add_subplot(325)
ax6 = fig.add_subplot(326)
ax1.plot(arrtime[:iend],arrI[:iend])
ax2.plot(arrtime[:iend],arrB[:iend])
ax3.plot(arrtime[:iend],arrQh[:iend])
ax4.plot(arrtime[:iend],arrQc[:iend])
ax5.plot(arrtime[:iend],arrJheat[:iend])
ax6.plot(arrtime[:iend],arrQ[:iend])

plt.show()
fig.savefig("docalcHeat.pdf")































