import sympy as sp
import numpy as np
from pint import UnitRegistry

ureg = UnitRegistry()
from typing import List
from Variable import Variable
from scipy.optimize import fsolve


class Relation:
    """ Class to define mathematical relations"""

    def __init__(self, varList: List[Variable], symEq: sp.Equality, *args, **kwargs):
        """ Input: varList: list of every Variable object in equality
                   symExpr: sp.Equality of the relation,
                   static: boolean describing if relation can be solved with the parameters given
                        in the Relation definition , default True,
                   desc: string describing this relation. """
        self._varList = []
        self._symEq = sp.Eq(0, 0)
        self._setVarList(varList)
        self._setEq(symEq)
        self._static = True
        self._desc = ""

        for argIndex in range(len(args)):
            # Check for value input
            if argIndex == 0:
                self.setStatic(args[argIndex])
            elif argIndex == 1:
                self.setDesc(args[argIndex])
            else:
                raise ValueError("Too many inputs")

        for key, val in kwargs.items():
            if key == 'static':
                self.setStatic(val)
            elif key == 'desc':
                self.setDesc(val)
            else:
                raise ValueError(f"Unknown input parameter '{key}'")

    def __str__(self):
        return str(self._symEq)

    def setStatic(self, status: bool):
        """ If true, sets this relation to a static relation.
            If false, sets this relation as a non-static relation."""
        if isinstance(status, bool):
            # Transfer value to instance variable
            self._static = status
        else:
            raise ValueError(f"Input must be of type 'bool', received type {type(status)}")

    def setDesc(self, newDesc: str):
        """ Updates the internal description of this Relation.
            Input: newDesc as a string"""
        if isinstance(newDesc, str):
            # Transfer value to instance variable
            self._desc = newDesc
        else:
            raise ValueError(f"Input must be of type 'str', recieved {type(newDesc)}")

    def _setVarList(self, varList: List[Variable]):
        """ Set this Relation's list of variables in the relation. Can only be called once"""
        if len(self._varList) == 0:
            for givenVar in varList:
                if isinstance(givenVar, Variable):
                    self._varList.append(givenVar)
                else:
                    raise ValueError("Given Variable must be of type Variable")
        else:
            raise ValueError("Method _setVarList can only be called once.")

    def _setEq(self, symEq: sp.Equality):
        """ Sets this Relation's sympy Equality. Also checks to make sure the equation only contains variables that
            are in this Relations given varList. Requires that the varList has already been added to self.
            Only called once by object constructor. """
        # Create list of Sympy representations of our varList
        symbolList = []
        for var in self._varList:
            symbolList.append(var.getSymRep())

        if isinstance(symEq, sp.Equality):
            # Create list of string representations of self's _varList
            varListStr = []
            for var in self._varList:
                varListStr.append(var.getSymRep())

            expr = symEq.lhs - symEq.rhs
            freeSymbols = expr.free_symbols
            for freeSym in freeSymbols:
                # Check for equality
                if freeSym.getSymRep() not in varListStr:
                    raise ValueError("Sympy Equation contains variables not given in this Relation's varList")
            # If it made it through the For loop, it is good to be assigned to this Relation!
            self._symEq = symEq
        else:
            raise ValueError(f"Given equality must be of type 'sp.Equality', recieved {type(symEq)}")

    def getEq(self) -> sp.Equality:
        """ Returns a sp.Equality object representing this Relation"""
        return self._symEq

    def getExpr(self) -> sp.Expr:
        """ Returns a Sympy Expression representation of this Relations Sympy equality"""
        return self._symEq.lhs - self._symEq.rhs

    def solveAuto(self, verbose=True):
        """ Solves the sympy Equation using the Variables originally inputted in this Relation's construction"""
        self.solve(self._varList)

    def solve(self, varList: List[Variable], verbose=True, guess=.1):
        """ Given a list of Variables, determines the 1 unknown Variable, solves for
            it, and updates the Variable value. All variables, including the 1 unknown variable,
            need to have Pint units.
            Input:
                varList: list of Variables
                verbose: boolean, determines if solving process is outputted to screen
                guess: Value passed to the interior fsolve equation. Usually can ignore this,
                    but is available here for testing purposes.
            """
        if len(varList) != len(self._varList):
            raise Exception("Given varList has different size than this Relation's varList")

        eq = self.getEq()
        expr = eq.lhs - eq.rhs

        # determine the known and unknown variables
        knownList = []
        unknownList = []
        unknownVarUnits = ureg.dimensionless
        index = 0
        unknownIndex = -1
        for var in varList:
            if var.pintQtyKnown():
                varPintQty = var.getPintQuantity()
                knownList.append((self._varList[index], varPintQty.to_base_units().magnitude))
            else:
                unknownList.append(var)
                # We need to know the unknown var's og units for reconversion
                unknownVarUnits = var.getUnits()
                unknownIndex = index
            index += 1

        # Check to make sure we have the proper amount of unknowns
        if len(unknownList) != 1:
            raise Exception(f"There must be exactly one unknown variable, but received {len(unknownList)} unknowns")

        # Substitute in the known vars
        exprSub = expr.subs(knownList)

        # Solve the expression for the unknown var
        func = sp.lambdify(self._varList[unknownIndex], exprSub, "numpy")
        unknownVarMag = fsolve(func, guess)[0]
        # Assign the proper units, with the knowledge that the calculation was performed in base units
        unknownVarBaseUnits = (1*unknownVarUnits).to_base_units()
        unknownVarPintQty = unknownVarMag * unknownVarBaseUnits.units
        unknownVarPintQty.ito(unknownVarUnits)

        # Assign new value to variable
        unknownList[0].setValue(unknownVarPintQty.magnitude)
        unknownList[0].convert_to(unknownVarPintQty.units)

        # Print off final value
        print(f"{unknownList[0]}")


