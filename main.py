import sympy as sp
import numpy as np
from pint import UnitRegistry
ur = UnitRegistry()
from Variable import Variable
from Relation import Relation

sp.init_printing()

theta = Variable("theta", ur.deg, desc="Slope half angle")
beta = Variable("beta", ur.deg, desc="Shock wave angle")
M = Variable("M", ur.dimensionless, desc="Mach number")
gamma = Variable("gamma", ur.dimensionless, 1.4, "specific heat ratio")

betaThetaMach = Relation([beta, theta, M, gamma], sp.Eq(sp.tan(theta), 2*(1/sp.tan(beta))*(M**2*(sp.sin(beta))**2 - 1)/(M**2*(gamma+sp.cos(2*beta))+2)))
print(betaThetaMach)

theta.setValue(30 * ur.deg)
M.setValue(4)
betaThetaMach.autoSolve()


sp.pprint(beta)
beta.convert_to(ur.rad)
print(beta)




v1 = Variable("v_1", ur.m ** 2 / ur.s ** 2, 45, desc="Velocity at point 1")
x1 = Variable("x_1", ur.ft / ur.s)
x2 = Variable("X_2", ur.miles / ur.year)

eq = sp.Eq(x1**2, v1)
relation = Relation([x1, v1], eq)
print()
# relation._setVarList([v1,x1])
relation._setEq(eq)

print(relation.getEq())
print(relation.getExpr())

print("ID")
print(id(x1))

relation.solve([x2, v1])




