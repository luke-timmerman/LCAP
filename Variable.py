import sympy as sp
import numpy as np
from pint import UnitRegistry
ureg = UnitRegistry()

class Variable(sp.Symbol):
    """ Class to contain all the basic information of a variable in the system. Inherits from
        sympy Symbol class so that these variables can be put into sympy expressions"""
    def __new__(cls, symRep: str, *args, **kwargs):
        """ Input: symRep: string,
                   units: ureg.Unit,
                   mag: int, float,
                   desc: string"""
        obj = sp.Symbol.__new__(cls, symRep)

        obj._mag = 0
        obj._magKnown = False
        obj._units = ureg.dimensionless
        obj._unitsKnown = False
        obj.symbol = symRep
        obj._desc = ""

        for argIndex in range(len(args)):
            # Check for value input
            if argIndex == 0:
                obj.setUnits(args[argIndex])
            elif argIndex == 1:
                obj.setMag(args[argIndex])
            elif argIndex == 2:
                obj.setDesc(args[argIndex])
            else:
                raise ValueError("Too many inputs")

        for key, val in kwargs.items():
            if key == 'mag':
                obj.setMag(val)
            elif key == 'units':
                obj.setUnits(val)
            elif key == 'desc':
                obj.setDesc(val)
            else:
                raise ValueError(f"Unknown input parameter '{key}'")

        return obj

    def __str__(self):
        outputStr = self.getSymRep()
        if self._magKnown or self._unitsKnown:
            outputStr = outputStr + " = "
        if self._magKnown:
            outputStr = outputStr + str(self.getMag()) + " "
        if self._unitsKnown:
            outputStr = outputStr + str(self.getUnits())
        return outputStr

    def setMag(self, newMag):
        """ Updates the magnitude of this Variable.
            Input: newValue as an int, float, or pint quantity """
        # Ensure value is an int, float, or pint quantity.
        if isinstance(newMag, int):
            # Transfer value to instance variable
            newMag = float(newMag)
            self._mag = newMag
            self._magKnown = True
        elif isinstance(newMag, float):
            self._mag = newMag
            self._magKnown = True
        else:
            # See if it is a quantity. We have to do it within a statement such as this for similar reasons as
            # self.setUnits
            try:
                newMagAsQty = ureg.Quantity(newMag.magnitude, newMag.units)
                # First convert our value
                self.convert_to(newMag.units)
                # Now change the magnitude
                self.setMag(newMag.magnitude)
            except:
                raise ValueError("Input must be of type 'int', 'float', or 'ureg.Quantity'")

    def setUnits(self, units: ureg.Unit):
        """ Sets the unit type of this Variable. This can only be done once! If you desire to change the unit system
            this variable is in, use Variable.convert_to(ureg.Unit)
            Input: newUnits as a pint ureg.Unit"""
        if self._unitsKnown == False:
            # Ensure value is a pint Unit
            # We first have to convert to a testQuantity, and then get the units from that. This is necessary because of
            # some Python quirk that won't recognize the unit as being an instance of ureg.Unit because it was imported
            # from a separate module
            try:
                testQuantity = ureg.Quantity(1, units)
            except TypeError:
                raise ValueError("Input must be of type 'ureg.Unit'")

            if isinstance(testQuantity.units, ureg.Unit):
                # Transfer value to instance variable
                self._units = units
                self._unitsKnown = True
            else:
                raise ValueError("Input must be of type 'ureg.Unit'")
        else:
            raise ValueError("Inputs already declared for this Variable. Use method convert_to to change unit systems")

    def convert_to(self, newUnits: ureg.Unit):
        """ Converts this quantity to the given unit system if it is allowable"""
        newQuantity = self.getPintQuantity().to(newUnits)
        self.setMag(newQuantity.magnitude)
        self._units = newQuantity.units

    def setDesc(self, newDesc: str):
        """ Updates the internal description of this Variable.
            Input: newDesc as a string"""
        if isinstance(newDesc, str):
            # Transfer value to instance variable
            self._desc = newDesc
        else:
            raise ValueError("Input must be of type 'str'")

    def pintQtyKnown(self):
        """ Returns true if this Variable has a Pint quantity associated with it"""
        if self._magKnown and self._unitsKnown:
            return True
        else:
            return False

    def getMag(self):
        """ Returns magnitude as a float"""
        if self._magKnown:
            return self._mag
        else:
            raise Exception("This Variable does not have a magnitude assigned to it.")

    def getUnits(self):
        """ Returns units as a ureg.Unit"""
        if self._unitsKnown:
            return self._units
        else:
            raise Exception("This Variable does not have units assigned to it.")

    def getPintQuantity(self):
        """ Returns the pint Quantity of this Variable"""
        return ureg.Quantity(self.getMag(), self.getUnits())

    def getSymRep(self):
        """ Returns the symbolic representation as a sympy.Symbol"""
        return self.symbol

    def getDesc(self):
        """ Returns the description as a string"""
        return self._desc

    def clearValue(self):
        """ Resets magnitude to be 0, marks the magnitude as unknown. The variable will retain the same
        dimensionality! """
        self.setMag(0)
        self._magKnown = False



class Variable_old:
    """ Class to contain all the basic information of a variable in the system. """
    def __init__(self, *args, **kwargs):
        """ Input: mag: int, float,
                   units: ureg.Unit
                   symRep: sp.Symbol,
                   desc: string"""
        self._mag = 0
        self._magKnown = False
        self._units = ureg.dimensionless
        self._unitsKnown = False
        self._symRep = sp.Symbol('')
        self._desc = ""

        for argIndex in range(len(args)):
            # Check for value input
            if argIndex == 0:
                self.setMag(args[argIndex])
            elif argIndex == 1:
                self.setUnits(args[argIndex])
            elif argIndex == 2:
                self.setSymRep(args[argIndex])
            elif argIndex == 3:
                self.setDesc(args[argIndex])
            else:
                raise ValueError("Too many inputs")

        for key, val in kwargs.items():
            if key == 'mag':
                self.setMag(val)
            elif key == 'units':
                self.setUnits(val)
            elif key == 'symRep':
                self.setSymRep(val)
            elif key == 'desc':
                self.setDesc(val)
            else:
                raise ValueError(f"Unknown input parameter '{key}'")

    def __str__(self):
        # return str(self.getSymRep()) + " = " + str(self.getPintQuantity())
        return str(self.getSymRep())

    def setMag(self, newMag):
        """ Updates the magnitude of this Variable.
            Input: newValue as an int, float, or pint quantity """
        # Ensure value is an int, float, or pint quantity.
        if isinstance(newMag, int):
            # Transfer value to instance variable
            newMag = float(newMag)
            self._mag = newMag
            self._magKnown = True
        elif isinstance(newMag, float):
            self._mag = newMag
            self._magKnown = True
        else:
            # See if it is a quantity. We have to do it within a statement such as this for similar reasons as
            # self.setUnits
            try:
                newMagAsQty = ureg.Quantity(newMag.magnitude, newMag.units)
                # First convert our value
                self.convert_to(newMag.units)
                # Now change the magnitude
                self.setMag(newMag.magnitude)
            except:
                raise ValueError("Input must be of type 'int', 'float', or 'ureg.Quantity'")

    def setUnits(self, units: ureg.Unit):
        """ Sets the unit type of this Variable. This can only be done once! If you desire to change the unit system
            this variable is in, use Variable.convert_to(ureg.Unit)
            Input: newUnits as a pint ureg.Unit"""
        if self._unitsKnown == False:
            # Ensure value is a pint Unit
            # We first have to convert to a testQuantity, and then get the units from that. This is necessary because of
            # some Python quirk that won't recognize the unit as being an instance of ureg.Unit because it was imported
            # from a separate module
            try:
                testQuantity = ureg.Quantity(1, units)
            except TypeError:
                raise ValueError("Input must be of type 'ureg.Unit'")

            if isinstance(testQuantity.units, ureg.Unit):
                # Transfer value to instance variable
                self._units = units
                self._unitsKnown = True
            else:
                raise ValueError("Input must be of type 'ureg.Unit'")
        else:
            raise ValueError("Inputs already declared for this Variable. Use method convert_to to change unit systems")

    def convert_to(self, newUnits: ureg.Unit):
        """ Converts this quantity to the given unit system if it is allowable"""
        newQuantity = self.getPintQuantity().to(newUnits)
        self.setMag(newQuantity.magnitude)
        self._units = newQuantity.units

    def setSymRep(self, newSymbol):
        """ Updates the sympy symbolic representation of this Variable
            Input: newSymbol as a string, or as a sp.Symbol"""
        if isinstance(newSymbol, str):
            # We must call the instantiator ourselves
            self._symRep = sp.Symbol(newSymbol)
        elif isinstance(newSymbol, sp.Symbol):
            self._symRep = newSymbol
        else:
            raise ValueError("Input must be of type 'str' or 'sympy.Symbol'")

    def setDesc(self, newDesc: str):
        """ Updates the internal description of this Variable.
            Input: newDesc as a string"""
        if isinstance(newDesc, str):
            # Transfer value to instance variable
            self._desc = newDesc
        else:
            raise ValueError("Input must be of type 'str'")

    def getMag(self):
        """ Returns magnitude as a float"""
        if self._magKnown:
            return self._mag
        else:
            raise Exception("This Variable does not have a magnitude assigned to it.")

    def getUnits(self):
        """ Returns units as a ureg.Unit"""
        if self._unitsKnown:
            return self._units
        else:
            raise Exception("This Variable does not have units assigned to it.")

    def getPintQuantity(self):
        """ Returns the pint Quantity of this Variable"""
        return ureg.Quantity(self.getMag(), self.getUnits())

    def getSymRep(self):
        """ Returns the symbolic representation as a string"""
        return self._symRep

    def getDesc(self):
        """ Returns the description as a string"""
        return self._desc

    def clearValue(self):
        """ Resets magnitude to be 0, marks the magnitude as unknown. The variable will retain the same
        dimensionality! """
        self.setMag(0)
        self._magKnown = False

