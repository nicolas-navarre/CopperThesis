#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:12:28 2019

@author: nicolasnavarre
"""

#Odeint function

import numpy
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def distribute(x,t,A,b,g,n):
 
    dxdt = A-b*x-g*x**(1/n)

    return dxdt
    
t = numpy.linspace(0,1/12,50)

xo = 0.5

y = odeint(distribute,xo,t)

plt.plot(t,y)
plt.show()
print(y)