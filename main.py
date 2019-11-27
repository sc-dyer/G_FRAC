from Garnet import Garnet
from GarnetCSD import GarnetCSD
from Sphere import Sphere
from Ellipsoid import Ellipsoid
from GeochemConst import *
from ComponentMol import ComponentMol
from GarnetComponentMol import GarnetComponentMol
from Traverse import Traverse
from CompoProfile import CompoProfile

import easygui
import os
import matplotlib.pyplot as plt
import re

# testSphere = Sphere(0.5)
# testCompo = [GarnetComponentMol(SPSS,0.25),GarnetComponentMol(PY,0.25),GarnetComponentMol(GR,0.25),GarnetComponentMol(ALM,0.25)]
# testGarnetBase = Garnet(testSphere,testCompo)
# testSphere.growByDim(2)
# print(testGarnetBase.totComposition[0].mol)
# biggerSphere = Sphere(2)
# nextShellCompo = [GarnetComponentMol(SPSS,0.7),GarnetComponentMol(PY,0.1),GarnetComponentMol(GR,0.1),GarnetComponentMol(ALM,0.1)]
# biggerGarnet = Garnet(testSphere,nextShellCompo,testGarnetBase)
# print(biggerGarnet.totComposition[0].mol)

# siConc = ComponentMol(Si, 2)
# print(siConc.mol)

#Begin the actual program
#Start by getting the traverse data:

print('Choose the csv file for the traverse')
#travIn = input('Enter the name and directory of the csv file for the traverse: ')
#travIn = easygui.fileopenbox('Choose the csv file for the traverse')
travIn = "/home/sabastien/Documents/Carleton/Probe/Central sections/Garnet_CSVs/18ZE-R-77A.csv"
if travIn != None:
	travIn = travIn.strip()
	travIn = travIn.strip('"')



	#gen = int(input("Enter the garnet generation to plot: "))

	#Make and plot the traverses
	trav = Traverse(travIn)
	travFig = plt.figure(figsize = (12,8))
	travAx = travFig.add_subplot()

	trav.plotAll(travAx)
	print("Please click on the plot where you want to split it in half, if you are satisfied with the plot as is, exit the window")
	plt.show()
	#Okay now we can have a thing for inputting composition values
	title = "THERIN Input"
	msg = "Please copy composition into the box below in same format as the THERIN file"
	#therin = easygui.enterbox(msg, title).strip()
	therin = "SI(1.0263)AL(0.31267)FE(0.14403)MN(0.00173)MG(0.0593)CA(0.02086)NA(0.05744)K(0.07516)TI(0.01002)C(100.0)H(200.0)O(102.833865)"
	#Now a code block to parse the THERIN
	composition = [] #Array to append Component mols
	therinList = re.split('\(|\)',therin)#Should make an array in form [component, mol, component, mol....]
	print(therinList)
	#Cycle through therinList array 2 at a time, to go from one component name to the next
	for i in range(0, len(therinList),2):
		#Compare to each component in COMPONENTS
		for j in range(len(COMPONENTS)):
			if therinList[i].strip().lower() == COMPONENTS[j].element.lower():
				#Convert the next entry into float and add to composition as a ComponentMol
				mol = float(therinList[i+1])
				thisComponent = ComponentMol(COMPONENTS[j], mol)
				composition.append(thisComponent)


	for i in range(len(composition)):
		print(composition[i].element + ": " + str(composition[i].mol))

	#Now ask user for rock volume
	msg = "Please input the volume of rock scanned (mm^3)"
	#scannedVol = float(easygui.enterbox(msg).strip())
	scannedVol = 51562
	#Code for selecting the blob file
	#blobIn = easygui.fileopenbox("Choose the xlsx file that the blob data is stored in")
	blobIn = "/home/sabastien/Documents/Carleton/Blob Output/18ZE-R-77A-dat.xls.xlsx"
	if blobIn != None:
		scannedCSD = GarnetCSD(blobIn,trav.selectedTrav,composition,scannedVol)
	else:
		print("No blob file chosen, ending program...")
else:
	print("No csv file chosen, ending program...")
	