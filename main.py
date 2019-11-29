from Garnet import Garnet
from GarnetCSD import GarnetCSD
from Sphere import Sphere
from Ellipsoid import Ellipsoid
from GeochemConst import *
from ComponentMol import *
from GarnetComponentMol import GarnetComponentMol
from Traverse import Traverse
from CompoProfile import CompoProfile
from SampleComp import SampleComp

import easygui
import os
import matplotlib.pyplot as plt
import pandas as pd
import re

SAMPLE_COL = "Name"

# testSphere = Sphere(0.5)
# testCompo = [GarnetComponentMol(SPSS,0.25),GarnetComponentMol(PY,0.25),GarnetComponentMol(GR,0.25),GarnetComponentMol(ALM,0.25)]
# testGarnetBase = Garnet(testSphere,testCompo)
# #testSphere.growByDim(2)
# print(testGarnetBase.totComposition[0].endMember + ": " + str(testGarnetBase.totComposition[0].mol))
# biggerSphere = Sphere(2)
# nextShellCompo = [GarnetComponentMol(SPSS,0.7),GarnetComponentMol(PY,0.1),GarnetComponentMol(GR,0.1),GarnetComponentMol(ALM,0.1)]
# biggerGarnet = testGarnetBase.growGarnet(nextShellCompo,1.5)#Garnet(testSphere,nextShellCompo,testGarnetBase)
# otherBigGrt = Garnet(biggerSphere,nextShellCompo,testGarnetBase)
# print(biggerGarnet.totComposition[0].endMember+ ": " + str(biggerGarnet.totComposition[0].mol))
# secondComponent  = biggerGarnet.getCompoAsComponentMol()
# componentMolList = testGarnetBase.getCompoAsComponentMol()
# bigComponent = otherBigGrt.getCompoAsComponentMol()

# print("First garnet:")
# for i in range(len(componentMolList)):
# 	print(componentMolList[i].element + ": " + str(componentMolList[i].mol))

# print("Second garnet:")
# for i in range(len(secondComponent)):
# 	print(secondComponent[i].element + ": " + str(secondComponent[i].mol))

# print("Third Garnet:")
# for i in range(len(bigComponent)):
# 	print(bigComponent[i].element + ": " + str(bigComponent[i].mol))

# print("Sum:")
# #componentList = biggerGarnet.getCompoAsComponentMol()
# componentList = addComponentList(bigComponent, secondComponent)
# for i in range(len(componentList)):
# 	print(componentList[i].element + ": " + str(componentList[i].mol))
# siConc = ComponentMol(Si, 2)
# siConc2 = ComponentMol(Si,5)
# siConc = siConc.sumComponents(siConc2)
# print("Si: " + str(siConc.mol))



# exit()
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

	#I am going to try to make this program take a geochemical csv file like THERIN_Generator, then allow the user to select from list
	#fileIn = easygui.fileopenbox('Select the csv file where the geochemical data is stored')
	fileIn = "/home/sabastien/Documents/Carleton/Geochem/Grt_bearing_geochem_Metapelites.csv"
	geochemDF = pd.read_csv(fileIn)

	samples = list(geochemDF[SAMPLE_COL])

	msg = "Select the sample to use"
	title = "Sample selection"
	chosenSample = easygui.choicebox(msg,title,samples)

	presentCmpnts = []
	wtCompo = []
	#Now should know which row to use
	selectedRow = geochemDF[geochemDF["Name"] == chosenSample]#Not sure if there is a better way
	
	for i in range(len(COMPONENTS)):
		if not(COMPONENTS[i].element == C.element or COMPONENTS[i].element == H.element):
			
			try:
				wtCompo.append(float(selectedRow[COMPONENTS[i].oxName]))
				presentCmpnts.append(COMPONENTS[i])
			except:
				print("Component " + COMPONENTS[i].oxName + " not found" )
	
	# #Renormalize to relevent components
	# normTot = sum(wtCompo)
	# for i in range(len(wtCompo)):
	# 	wtCompo[i] = wtCompo[i]/normTot*100



	#Okay now we can have a thing for user input
	title = "User Input"
	msg = "Please provide the following information"
	fieldNames = ["Scanned Volume (cm^3)","Density (g/cm^3)","Sample Name"]

	# fieldValues = easygui.multenterbox(msg,title, fieldNames)
	# # make sure that none of the fields was left blank
	# while 1:
 #    	if fieldValues == None: break
 #    	errmsg = ""
 #    	for i in range(len(fieldNames)):
 #      	if fieldValues[i].strip() == "":
 #        	errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
 #    	if errmsg == "": break # no problems found
 #    	fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
	
 #    therin = fieldValues[0].strip()
 #    volume = float(fieldValues[0].strip())
 #    density = float(fieldValues[1].strip())
 #    name = fieldValues[2].strip()

	therin = "SI(1.0263)AL(0.31267)FE(0.14403)MN(0.00173)MG(0.0593)CA(0.02086)NA(0.05744)K(0.07516)TI(0.01002)C(100.0)H(200.0)O(102.833865)"
	volume = 51.562
	density = 2.20
	name = "18ZE-R-77A"

	mass = density*volume

	sampleCompo = SampleComp(name,wtCompo,presentCmpnts,mass)

	redCo2 = True
	h2o = 100
	co2 = 100

	sampleCompo.calcO2(redCo2,co2,h2o)
	composition = sampleCompo.molArray
	for i in range(len(composition)):
		print(composition[i].element + ": " + str(composition[i].mol))

	#Now a code block to parse the THERIN
	# composition = [] #Array to append Component mols
	# therinList = re.split('\(|\)',therin)#Should make an array in form [component, mol, component, mol....]
	# #print(therinList)
	# #Cycle through therinList array 2 at a time, to go from one component name to the next
	# for i in range(0, len(therinList),2):
	# 	#Compare to each component in COMPONENTS
	# 	for j in range(len(COMPONENTS)):
	# 		if therinList[i].strip().lower() == COMPONENTS[j].element.lower():
	# 			#Convert the next entry into float and add to composition as a ComponentMol
	# 			mol = float(therinList[i+1])
	# 			thisComponent = ComponentMol(COMPONENTS[j], mol)
	# 			composition.append(thisComponent)

	#Okay now here we will convert the relative mol fraction into the absolute number of mols for the given rock volume and density
	#So I have two choices, either I can prompt the user to provide wt% instead of # mols or I can go the other direction and convert the mols into wt% and then reconvert back to mols
	#The second one sems like too much work but the first one leaves either a lot of entries to the user or something idk
	#First one seems more straightforward
	



	#Code for selecting the blob file
	#blobIn = easygui.fileopenbox("Choose the xlsx file that the blob data is stored in")
	blobIn = "/home/sabastien/Documents/Carleton/Blob Output/18ZE-R-77A-dat.xls.xlsx"
	#outputDir = easygui.diropenbox("Select the directory to save output")
	outputDir = "/home/sabastien/Documents/Carleton/Modelling/Garnet Fractionation/77A/"
	if blobIn != None:
		#now make the csd
		scannedCSD = GarnetCSD(blobIn,trav.selectedTrav,composition,volume, name)

		radInterval = 0.1
		scannedCSD.fractionateGarnet(radInterval,outputDir)
	else:
		print("No blob file chosen, ending program...")
else:
	print("No csv file chosen, ending program...")
	