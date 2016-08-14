# -*- coding: cp936 -*-
#calcMainUsingExcel.py

import wx
import os
from win32com.client import Dispatch 
import win32com.client
import time
from numpy import *
import math

import calcHeat
import getPhysicalParameters
import calcCoilAndShell
import calcInnerHeat
import calcHelium


class easyExcel: 
    """A utility to make it easier to get at Excel.  Remembering 
    to save the data is your problem, as is  error handling. 
    Operates on one workbook at a time.""" 
    def __init__(self, filename=None): 
        self.xlApp = win32com.client.Dispatch('Excel.Application') 
        if filename: 
            self.filename = filename 
            self.xlBook = self.xlApp.Workbooks.Open(filename) 
        else: 
            self.xlBook = self.xlApp.Workbooks.Add() 
            self.filename = ''  
    def save(self, newfilename=None): 
        if newfilename: 
            self.filename = newfilename 
            self.xlBook.SaveAs(newfilename) 
        else: 
            self.xlBook.Save()    
    def close(self): 
        self.xlBook.Close(SaveChanges=0) 
        del self.xlApp 
    def getCell(self, sheet, row, col): 
        "Get value of one cell" 
        sht = self.xlBook.Worksheets(sheet) 
        return sht.Cells(row, col).Value 
    def setCell(self, sheet, row, col, value): 
        "set value of one cell" 
        sht = self.xlBook.Worksheets(sheet) 
        sht.Cells(row, col).Value = value 



if __name__ == "__main__": 
    #PNFILE = r'c:\screenshot.bmp' 
    xls = easyExcel(r'C:/Python27/HEPAK Example.xls') 
    #xls.addPicture('Sheet1', PNFILE, 20,20,1000,1000) 
    #xls.cpSheet('Sheet1')
    '''
    print xls.getCell(1,9,3)
    print xls.getCell(1,20,4)
    print xls.getCell(1,21,4)

    xls.setCell(1,9,3,i)
    print xls.getCell(1,9,3),'\t',xls.getCell(1,20,4),'\t',xls.getCell(1,21,4)

    xls.setCell(1,9,3,2*i)
    print xls.getCell(1,9,3),'\t',xls.getCell(1,20,4),'\t',xls.getCell(1,21,4)

    attempts =0
    success = False
    for j in range(10000):
        #time.sleep(1)
        try:
            xls.setCell(1,9,3,i+20*j)
            print xls.getCell(1,9,3),'\t',xls.getCell(1,20,4),'\t',xls.getCell(1,21,4)
        except:
            xls.setCell(1,9,3,i+20*(j-1))
            print xls.getCell(1,9,3),'\t',xls.getCell(1,20,4),'\t',xls.getCell(1,21,4)
            print "fail to get value in p= %f" %(i+20*j)



    '''
    #Now, let's put in the Calc_code  
    #--------------------------------------------------------------------------------------------------------------------
    # 1. GET ALL DATA INITIALIZED
    L = 400
    dx = 40
    p_gasIn = 0.26*10**6
    p_gasOut = 0.50*10**6
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
    spd = [0]*m
    for i in range(m):
        spd[i] = 18*0.001/4/(0.3*(17.6*10.6*10**(-6))*heliumDst[i])
    #coilT
    coilT= [4.5]*m
    coilT[int(m/2)]= 20
    #shellT
    shellT = [[4.5 for col in range(4)] for row in range(m)]
    
    print 'helium T ','\n', heliumT
    print 'helium P ','\n',heliumP
    print 'helium density ','\n',heliumDst
    print 'coilT ','\n',coilT
    print 'ShellT ','\n',shellT
    print 'helium speed ','\n',spd
    

    #----------------------------------------------------------------------------------------------------------------------
    # 2. {{{ CALC THE PHASE IN INNERHEAT &&  HELIUM TEMP-RISE  }}}  RECYCLE (time/dt) TIMES
    time = 0
    for i in range(3):
        #first , calc the coil with innerHeat for (dt/ddt) times , get [[[ coilT,shellT, St1Sum, St2Sum ]]]
        dt = 0.1
        ddt = 0.01
        dynVis = [0]*m
        con = [0]*m
        Cp = [0]*m
        hCoil = [0]*m
        St1Sum = [0]*m
        St2Sum = [0]*m
        mCu = dx*80*pi*0.16*10**(-6)*8900
        mSc = dx*160*pi*0.16*10**(-6)*9140
        mShell = dx*(2.2*(10+17)*10**(-6))*7916*0.33333
        mm = int(dt/ddt)
        for ii in range(mm):
            print "time = ",time
            # coil get temperature-rise from InnerHeat
            coilT = calcCoilAndShell.calcCoilT_InnerHeat(coilT, m , time, dx, ddt , mCu, mSc)
            '''
            print "coil   自发热之后"
            print coilT
            print heliumT
            '''
            # coil get temperature-change from conductivity between all dx-coil
            coilT = calcCoilAndShell.calcNextCoilT(coilT,m,dx, ddt, mCu, mSc)
            '''
            print "coil   自身导热传播"
            print coilT
            '''
            # coil get temperature-decrease from cold helium
            dh = 4*((0.3*17.6*10.6*10**(-6))/(pi*0.8*0.001*240))
            for hi in range(m):
                xls.setCell(1,9,3,heliumP[hi])
                xls.setCell(1,9,4,heliumT[hi])                  
                dynVis[hi] = xls.getCell(1,42,4)
                con[hi] = xls.getCell(1,43,4)
                Cp[hi] = xls.getCell(1,31,4)
                hCoil[hi] = calcCoilAndShell.calc_hCoil(heliumDst[hi],spd[hi],dh,dynVis[hi],Cp[hi],con[hi])
            coilT, StOne = calcCoilAndShell.calcConvectionWithCoil(coilT, heliumT , m,dx, ddt, mCu , mSc, hCoil)
            '''
            print "coil 和氦气热交换之后"
            print coilT
            print "st1"
            print StOne
            '''
            # shell get temperature-change from hot helium
            shellT, StTwo = calcCoilAndShell.calcShellT(shellT,  heliumT ,m, dx,dt ,mShell)
            #print "st2"
            #print StTwo
            for j in range(m):
                St1Sum[j] += StOne[j]
                St2Sum[j] += StTwo[j]
            time += ddt
            
            print "-------------------------------------------------------------"
        
        
        print "******************************************************************"
        # second , calc the helium in dt ， get  [[[ heliumT, heliumP, heliumDst, spd ]]]
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
            St = St1Sum[i]/((17.6*10.6*0.3)*10**(-6))
            #print "St " ,i ," = ",   St ,"    st1=   ",St1Sum[i],"    st2=   ",St2Sum[i]           
            nextT[i],nextDensity[i],nextSpd[i]=calcHelium.calcHeliumGeneral(dt,dx,heliumT[i-1],heliumT[i],heliumT[i+1],
                                                                     heliumP[i-1],heliumP[i],heliumP[i+1],
                                                                     heliumDst[i-1],heliumDst[i],heliumDst[i+1],
                                                                     spd[i-1],spd[i],spd[i+1],
                                                                     dynVis,con,Cp,St)
            
                               
        #deal with the begin_point and end_point
        xls.setCell(1,9,3,heliumP[0])
        xls.setCell(1,9,4,heliumT[0])                  
        dynVis = xls.getCell(1,42,4)
        con = xls.getCell(1,43,4)
        Cp = xls.getCell(1,31,4)
        St = (St1Sum[0])/((17.6*10.6*0.3)*10**(-6))
        nextT[0],nextDensity[0],nextSpd[0]=calcHelium.calcHeliumBeginPoint(dt,dx,0,heliumT[0],heliumT[1],
                                                                     0,heliumP[0],heliumP[1],
                                                                     0,heliumDst[0],heliumDst[1],
                                                                     0,0,spd[1],
                                                                     dynVis,con,Cp,St)
        nextSpd[0]=0
        nextT[0]=float(nextT[1])
        xls.setCell(1,9,3,heliumP[m-1])
        xls.setCell(1,9,4,heliumT[m-1])                  
        dynVis = xls.getCell(1,42,4)
        con = xls.getCell(1,43,4)
        Cp = xls.getCell(1,31,4)
        St = (St1Sum[m-1])/((17.6*10.6*0.3)*10**(-6))
        nextT[m-1],nextDensity[m-1],nextSpd[m-1]=calcHelium.calcHeliumEndPoint(dt,dx,heliumT[m-2],heliumT[m-1],0,
                                                                     heliumP[m-2],heliumP[m-1],0,
                                                                     heliumDst[m-2],heliumDst[m-1],0,
                                                                     spd[m-2],spd[m-1],0,
                                                                     dynVis,con,Cp,St)
        nextSpd[m-1]=0
        nextT[m-1]=float(nextT[m-2])

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

        for gi in range(m):
            print "heliumT[%d] = "%(gi),heliumT[gi]
        for gi in range(m):
            print "spd[%d] = "%(gi),spd[gi]
        print "******************************************************************"
        
    
xls.close()





















'''
    #尝试内置button
    class myapp(wx.App):
                        def OnInit(self):
                                frame=wx.Frame(parent=None,
                                                                id=-1,
                                             title='BUTTON',
                                    pos=(100,100),
                                    size=(800,880),
                                    style=wx.DEFAULT_FRAME_STYLE,
                                    name="framebutton")
                        
                                panel=wx.Panel(frame,-1)
                        
                                self.button1=wx.Button(panel,
                                                                -1,
                                                                'Button1',
                                                                 pos=(500,500),
                                                                size=(200,200)
                                                              )
                                self.Bind(wx.EVT_BUTTON,self.OnButton1,self.button1)
                        
                                self.button2=wx.Button(panel,
                                                                -1,
                                                                'Button2',
                                                                 pos=(100,500),
                                                                size=(200,200)
                                                              )
                                self.Bind(wx.EVT_BUTTON,self.OnButton2,self.button2)
                                self.button1.SetDefault()

                                #self.label=wx.StaticText(panel,-1,'vhjkbkl',pos=(200,200))

                        
                                frame.Show()
                                return True

                        def OnButton1(self,event):
                                self.button2.SetLabel('Button1')
                                self.button2.SetDefault()
                                self.button1.SetLabel('Button2')

                        def OnButton2(self,event):
                                self.button1.SetLabel('Button1')
                                self.button1.SetDefault()
                                self.button2.SetLabel('Button2')        
                                                              
                        
    app=myapp()
    app.MainLoop()
    '''
