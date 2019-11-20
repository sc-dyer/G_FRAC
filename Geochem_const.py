#Geochem_const.py
#Contains definitions of the different components

from Component import Component
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
GT_ENDMEM = ['spss','py','gr','alm']#End member codes for garnet in domino
CMPNT = ["Mn","Mg","Ca","Fe"] #Components of garnet, this corresponds to the order they are placed in the cmpnts array
GRT_CMPNTS =[Mn,Mg,Ca,Fe]
GRT_DENSITY = 4.19 #Density in g/cm^3
M_SPSS = Mn.weight*3 + Al.weight*2 + Si.weight*3 + O.weight*12
M_PY = Mg.weight*3 + Al.weight*2 + Si.weight*3 + O.weight*12
M_GR = Ca.weight*3 + Al.weight*2 + Si.weight*3 + O.weight*12
M_ALM = Fe.weight*3 + Al.weight*2 + Si.weight*3 + O.weight*12
GRT_M = [M_SPSS,M_PY,M_GR,M_ALM]
