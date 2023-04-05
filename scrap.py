# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 09:01:08 2022

@author: luket
"""

from pint import UnitRegistry
ureg = UnitRegistry()
import math
import matplotlib.pyplot as plt
import sympy as sp
sp.init_printing(use_latex=True)
import numpy as np
from scipy.optimize import fsolve, fmin
import inspect
#from functions import *

#M1 = 2.5
#p1 = 1 * ureg.atm
#T1 = 300 * ureg.kelvin
#theta = 22.5 * ureg.deg
#gamma = 1.4
#
#
#thetaSym, betaSym, MSym, gammaSym = sp.symbols('theta Beta M_1 gamma')
#btm = sp.Eq(sp.tan(thetaSym), 2*(1/sp.tan(betaSym))*(MSym**2 * sp.sin(betaSym)**2 -1)/(MSym**2 * (gammaSym+sp.cos(2*betaSym))+2))
#btmExpr = btm.rhs - btm.lhs
#btmExpr = btmExpr.subs([(thetaSym, theta), (MSym, M1), (gammaSym, gamma)])
#btmF = sp.lambdify(betaSym, btmExpr, "numpy")
#beta = fsolve(btmF, .1)[0] * ureg.rad
#
#
#M1n = M1*math.sin(beta)
#M2n = M2f(M1n, gamma)
#M2 = M2n / math.sin(beta-theta)
#print(M2)


print("HI")

# We're on the branch!