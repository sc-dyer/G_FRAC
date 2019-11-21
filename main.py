from Garnet import Garnet
from Sphere import Sphere
from Ellipsoid import Ellipsoid
from GeochemConst import *
from ComponentMol import ComponentMol
from GarnetComponentMol import GarnetComponentMol

testSphere = Sphere(0.5)
testCompo = [GarnetComponentMol(SPSS,0.25),GarnetComponentMol(PY,0.25),GarnetComponentMol(GR,0.25),GarnetComponentMol(ALM,0.25)]
testGarnetBase = Garnet(testSphere,testCompo)
testSphere.growByDim(2)
print(testGarnetBase.totComposition[0].mol)
biggerSphere = Sphere(2)
nextShellCompo = [GarnetComponentMol(SPSS,0.7),GarnetComponentMol(PY,0.1),GarnetComponentMol(GR,0.1),GarnetComponentMol(ALM,0.1)]
biggerGarnet = Garnet(testSphere,nextShellCompo,testGarnetBase)
print(biggerGarnet.totComposition[0].mol)

siConc = ComponentMol(Si, 2)
print(siConc.mol)