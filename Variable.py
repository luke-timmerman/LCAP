import sympy as sp
import numpy as np
from pint import UnitRegistry
ureg = UnitRegistry()

class Variable(sp.Symbol):
    """ Class to contain all the basic information of a variable in the system. Inherits from
        sympy Symbol class so that these variables can be put into sympy expressions"""
    def __new__(cls, symRep: str, units: ureg.Unit, *args, **kwargs):
        """ Input: symRep: string,
                   units: ureg.Unit,
                   mag: int, float,
                   desc: string"""
        obj = sp.Symbol.__new__(cls, symRep)

        obj._mag = 0
        obj._magKnown = False
        obj._units = ureg.dimensionless
        obj._setUnits(units)
        obj.symbol = symRep
        obj._desc = ""


        for argIndex in range(len(args)):
            # Check for value input
            if argIndex == 0:
                obj.setValue(args[argIndex])
            elif argIndex == 1:
                obj.setDesc(args[argIndex])
            else:
                raise ValueError("Too many inputs")

        for key, val in kwargs.items():
            if key == 'mag':
                obj.setValue(val)
            elif key == 'desc':
                obj.setDesc(val)
            else:
                raise ValueError(f"Unknown input parameter '{key}'")

        return obj

    def getVarValueStr(self):
        """ Returns a string representation of this variable and its value """
        outputStr = self.getSymRep()
        outputStr = outputStr + " = "
        if self._magKnown:
            outputStr = outputStr + str(self.getMag()) + " "
        outputStr = outputStr + str(self.getUnits())
        return outputStr

    def setValue(self, newVal):
        """ Updates the magnitude of this Variable. If newVal is a pint quantity, it will first be converted
            to this Variable's unit system. Call convert_to to change the unit system
            Input: newValue as an int, float, or pint quantity """
        # Ensure value is an int, float, or pint quantity.
        if isinstance(newVal, int):
            # Transfer value to instance variable
            newVal = float(newVal)
            self._mag = newVal
            self._magKnown = True
        elif isinstance(newVal, float):
            self._mag = newVal
            self._magKnown = True
        else:
            # See if it is a quantity. We have to do it within a statement such as this for similar reasons as
            # self.setUnits
            try:
                newMagAsQty = ureg.Quantity(newVal.magnitude, newVal.units)
                # First convert our value
                newMagAsQty.ito(self._units)
                # Now change the magnitude
                self.setValue(newMagAsQty.magnitude)
            except:
                raise ValueError("Input must be of type 'int', 'float', or 'ureg.Quantity'")

    def _setUnits(self, units: ureg.Unit):
        """ Sets the unit type of this Variable. This can only be done once! If you desire to change the unit system
            this variable is in, use Variable.convert_to(ureg.Unit)
            Input: newUnits as a pint ureg.Unit"""
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
        else:
            raise ValueError(f"Input must be of type 'ureg.Unit', received {type(units)}")

    def convert_to(self, newUnits: ureg.Unit):
        """ Converts this Variable to the given unit system if it is allowable"""
        if self._magKnown:
            oldQuantity = self.getPintQuantity()
        else:
            oldQuantity = 0 * self._units
        newQuantity = oldQuantity.to(newUnits)
        self.setValue(newQuantity.magnitude)
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
        if self._magKnown:
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
        return self._units

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
        self.setValue(0)
        self._magKnown = False
