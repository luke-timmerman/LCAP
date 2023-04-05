import sympy as sp
import numpy as np
from pint import UnitRegistry
ur = UnitRegistry()

class System():
    """ Class which contains the basic elements of a system - i.e. the Variables, Relations, Functions.
        A System is meant to provide a space where everything is contained and follows certain basic laws.
        So, you can have a global system which contains every variable and subsystem, as well as systems to
        represent specific situations, such as an orbital transfer system, or a oblique shock wave system.
        You can also have Systems which represent certain states of a problem.

        For example, for a normal shock wave system, you could have a system to represent state 1 which contains a
        Mach number, density, etc, as well as a system for state 2 which contains its own Mach number, density, etc.
        Then, both of these states would be inputted into the Shock Wave System, which would take them and create
        relations between the two states. All of the relations which are created would be inserted into the global
        system.

        Since a system contains all the basic Variables, Relations, and Functions of a system, a System will also
        contain methods to solve for variables, using the relations and functions that are a part of it. """