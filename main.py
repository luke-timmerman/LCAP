import sympy as sp
import numpy as np
from pint import UnitRegistry
ureg = UnitRegistry()
from Variable import Variable
from Relation import Relation

sp.init_printing()

v1 = Variable("v_1",ureg.m**2 / ureg.s**2, 45, desc="Velocity at point 1")
x1 = Variable("x_1", ureg.ft/ureg.s)
x2 = Variable("X_2", ureg.miles/ureg.year)

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




