from Garnet import Garnet
from Sphere import Sphere
from Ellipsoid import Ellipsoid
from Geochem_const import *

testSphere = Sphere(0.5)
testCompo = [0.25,0.25,0.25,0.25]
testGarnetBase = Garnet(testSphere,testCompo)
testSphere.growByDim(2)
print(testGarnetBase.totMol)
biggerSphere = Sphere(2)
nextShellCompo = [0.7,0.1,0.1,0.1]
biggerGarnet = Garnet(testSphere,nextShellCompo,testGarnetBase)
print(biggerGarnet.totMol)