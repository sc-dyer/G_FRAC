#GeochemConst.py
#Contains definitions of the different components

from Component import Component
from GarnetComponent import GarnetComponent
from ComponentMol import ComponentMol

#Making the components: Input values are name, molar weight, oxide ratio, cation number, Cation name
Si = Component("Si", 28.086, 2, 1)
Al = Component("Al", 26.982, 3/2, 2)
Fe = Component("Fe", 55.933, 1, 2) 
Mn = Component("Mn", 54.938, 1, 1)
Mg = Component("Mg", 24.305, 1, 1)
Ca = Component("Ca", 40.078, 1, 1)
Na = Component("Na", 22.990, 1/2, 2)
K = Component("K", 39.098, 1/2, 2)
Ti = Component("Ti", 47.88, 2, 1)
P = Component("P", 30.974, 5/2, 2)
H = Component("H", 1.008, 1/2, 2)
C = Component("C",12.011, 2, 1)
O = Component("O",15.999,1,1) #Oxide is O2 1:1 ratio

COMPONENTS = [Si, Al, Fe, Mn, Mg, Ca, Na, K, Ti, H, C, O] #No P2O5 because unreliable data, add if desired
GRT_DENSITY = 4.19 #Density in g/cm^3


SPSS = GarnetComponent("Mn","spss",[ComponentMol(Mn,3),ComponentMol(Al,2),ComponentMol(Si,3),ComponentMol(O,12)])
PY = GarnetComponent("Mg","py",[ComponentMol(Mg,3),ComponentMol(Al,2),ComponentMol(Si,3),ComponentMol(O,12)])
GR = GarnetComponent("Ca","gr",[ComponentMol(Ca,3),ComponentMol(Al,2),ComponentMol(Si,3),ComponentMol(O,12)])
ALM = GarnetComponent("Fe","alm",[ComponentMol(Fe,3),ComponentMol(Al,2),ComponentMol(Si,3),ComponentMol(O,12)])

GRT_CMPNT = [SPSS,PY,GR,ALM]