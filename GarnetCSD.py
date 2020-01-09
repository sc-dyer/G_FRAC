#This is a class for reading and modelling garnet CSDs
#It can read a blob output file and use Garnet.py to model garnet growth
#Maybe it will do more in the far future but this is the goal for now

from Garnet import Garnet
from GeochemConst import *
from Shape import Shape
from Sphere import Sphere
from Ellipsoid import Ellipsoid
from CompoProfile import CompoProfile
from ComponentMol import *
from GarnetComponentMol import GarnetComponentMol
from SCRIPT_Generator import *

import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import easygui
import math
import copy

NUM_SHELLS = 3000 #This is the number of garnet shells the biggest garnet will have 
#DATABASE = "tcdb55c2_COHmelt.txt"
T1 = 450
T2 = 650
P1 = 2000
P2 = 10000

CORE_AVG_INDEX = 3 #Number of cells to average for the core composition
class GarnetCSD:

	def __init__(self,blobFileName,garnetProfile,rockCompo, rockVolume, sampleName):

		self.composition = rockCompo #This is a list of ComponentMol objects that define the rock composition
		self.grtProfile = garnetProfile #This is the CompoProfile object that is a half profile that defines the zoning in the garnet
		self.rockVol = rockVolume
		#Now need to open up the blob file to build the crystal list
		blobDF = pd.read_excel(blobFileName) #Assumes that formatting has not changed from default blob output
		self.name = sampleName
		self.crystalList = [] #Empty list to fill with Shape entries

		blobDF = blobDF.dropna() #Sometimes empty rows at the end mess up calculations
			
		#Ask user to choose if using spheres or ellipsoids
		msg = "Are garnets spheres or ellipsoids?"
		title = ""
		choices = ["Sphere","Ellipsoid"]
		reply = easygui.buttonbox(msg,title,choices)
		#reply = "Sphere" #Only works for Spheres right now, need to think about size independent growth of ellipsoids
		if(reply==choices[0]):
			volume = list(blobDF['Volume (mm^3)'])

			for i in range(len(volume)):
				#If spheres, it will recalculate the radius from the volume
				#if not math.isnan(volume[i]):
				thisRad = (volume[i]*3/(4*math.pi))**(1./3)
				self.crystalList.append(Sphere(thisRad))

		elif(reply == choices[1]):
			#If ellipsoid it uses the PEllipsoid data
			# #It should be that rad1 > rad2 > rad3
			# rad1 = list(blobDF['PEllipsoid Rad1 (mm)'])
			# rad2 = list(blobDF['PEllipsoid Rad2 (mm)'])
			# rad3 = list(blobDF['PEllipsoid Rad3 (mm)'])
			
			# for i in range(len(rad1)):
			# 	if not math.isnan(rad1[i]):
			# 		self.crystalList.append(Ellipsoid(rad1[i],rad2[i],rad3[i]))

			#Average out the ratios so all ellipsoids are the same shape and grow with the same dimensions
			avgEllipsoid = self.getAvgEllipsoid(blobDF)
			volume = list(blobDF['Volume (mm^3)'])

			for i in range(len(volume)):
				#Need to rescale the avg ellipsoid to fit the volume of each garnet
				#if not math.isnan(volume[i]):
				ratioAB = avgEllipsoid.aAx/avgEllipsoid.bAx
				ratioBC = avgEllipsoid.bAx/avgEllipsoid.cAx
				thisA = ((3*ratioAB**2*ratioBC*volume[i])/(math.pi*4))**(1/3)
				thisB = thisA/ratioAB
				thisC = thisB/ratioBC
					
				self.crystalList.append(Ellipsoid(thisA,thisB,thisC))
		else:
			print("Error: No option chosen")
			return

		#Okay now we need to stretch the garnet profile to fit with the long dimension of the ellipsoid or the radius of the sphere
		#This is so the profile matches up with the biggest garnet

		self.quickSortCrystals(0,len(self.crystalList)-1)
		travRad = max(self.grtProfile.x) #Radius of the garnet measured in the microprobe profile
		self.shellThick = self.crystalList[0].getDim()/NUM_SHELLS 
		#Instead of stretching, lets try extrapolating the core inwards:
		radAdd = self.crystalList[0].getDim() - travRad
		if radAdd > 0: #In case the biggest garnet has a radius smaller than traverse length
			self.grtProfile.extrapCore(CORE_AVG_INDEX, radAdd)
		else: 
			scaleFactor = self.crystalList[0].getDim()/travRad #The scaling factor to convert the x values in grtProfile to be the same size as the radius or a axis of ellipsoid
			
			for i in range(len(self.grtProfile.x)): 
				#Rescale x
				self.grtProfile.x[i] = scaleFactor*self.grtProfile.x[i]

		self.grtProfile.scipyInterp() #Initialize the interpolated numpy arrays

		self.garnetList = [] #This is what we will be working with for the most part, it is where all the garnets will grow and be stored


	def quickSortCrystals(self, low, high):
		#Function to sort the garnets by volume
		#Lets do a quick sort because thats fun
		#better to sort biggest to smallest
		if low < high:

			i = low - 1
			pivot = self.crystalList[high].getVolume() #Compare every element in list to the pivot
			
			for j in range(low,high):

				if(self.crystalList[j].getVolume() >= pivot):
					#Increment i by 1 if j is bigger than pivot
					#Then swap element at i and j

					i = i + 1
					self.crystalList[i], self.crystalList[j] = self.crystalList[j], self.crystalList[i]

			#Swap element at high and element at i + 1
			#Putting all elements bigger in volume to left of the element at high
			self.crystalList[i+1], self.crystalList[high] = self.crystalList[high], self.crystalList[i+1]

			pi = i + 1
			
			self.quickSortCrystals(low, pi-1)
			self.quickSortCrystals(pi+1, high)

	def fractionateGarnet(self, radInterval, outputDir, database):
		#A method to fractionate garnet and output the composition at each radInterval
		count = 1
		self.growGarnetShell()
		while(self.garnetList[0].bigAx < self.crystalList[0].getDim()-self.shellThick):
			#Grow garnet until the biggest garnet is one shell away from its max size
			self.growGarnetShell()
			
			if(abs(self.garnetList[0].bigAx-radInterval*count)<self.shellThick):
				

				#print("Biggest Radius = " + str(self.garnetList[0].bigAx))
				#print(self.garnetList[0].composition[0].endMember + ": " + str(self.garnetList[0].composition[0].molFrac))
				#print("Number of garnets: " + str(len(self.garnetList)))

				self.calcTotalGarnetMol()
				
				

				self.writeScriptFiles(outputDir, count, database)


				print(str(len(self.garnetList)) + " garnets grown")

				# print("Volumes are:")
				# for garn in self.garnetList:
				# 	print(garn.totVol)
				# print("Outer Shell:")
				# for garn in self.garnetList:
				# 	print(str(garn.composition[0].molFrac) + "," + str(garn.composition[1].molFrac) + "," + str(garn.composition[2].molFrac) + "," + str(garn.composition[3].molFrac))
				
				# print("Radius:")
				# for garn in self.garnetList:
				# 	print(garn.bigAx)
				# print("Mol Sum:")
				# for garn in self.garnetList:
				# 	thisCompo = garn.getCompoAsComponentMol()
				# 	compoString = ""
				# 	for cmpnt in thisCompo:
				# 		compoString += cmpnt.element +": " + str(cmpnt.mol) + ", "
				# 	print(compoString)

				# for i in range(len(self.totGarnetMol)):
				# 	print("Total mol of " + self.totGarnetMol[i].element + " = " + str(self.totGarnetMol[i].mol))

				count += 1

		self.calcTotalGarnetMol()		
		self.writeScriptFiles(outputDir, count, database)
		print(str(len(self.garnetList)) + " garnets grown")

		# print("Volumes are:")
		# for garn in self.garnetList:
		# 	print(garn.totVol)
		# print("Outer Shell:")
		# for garn in self.garnetList:
		# 	print(str(garn.composition[0].molFrac) + "," + str(garn.composition[1].molFrac) + "," + str(garn.composition[2].molFrac) + "," + str(garn.composition[3].molFrac))
				
		# print("Radius:")
		# for garn in self.garnetList:
		# 	print(garn.bigAx)
		# print("Mol Sum:")
		# for garn in self.garnetList:
		# 	thisCompo = garn.getCompoAsComponentMol()
		# 	compoString = ""
		# 	for cmpnt in thisCompo:
		# 		compoString += cmpnt.element +": " + str(cmpnt.mol) + ", "
		# 	print(compoString)
		# for i in range(len(self.totGarnetMol)):
		# 			print("Total mol of " + self.totGarnetMol[i].element + " = " + str(self.totGarnetMol[i].mol))

		print("Done growing garnets")

	def growGarnetShell(self):
		#Function to grow an additional shell of garnet
		#Will add a new garnet once the radius difference between the last garnet and the next one is sufficient

		if len(self.garnetList) == 0: #Initialize first garnet
			firstShellCompo = self.getShellCompo(self.shellThick,0)
			self.nucleateGarnet(self.crystalList[0],firstShellCompo)
			print("First garnet nucleated")
		else:
			#First calculate the next composition interval
			biggestRad = self.garnetList[0].bigAx
			nextShellRad = biggestRad + self.shellThick
			nextShellCompo = self.getShellCompo(nextShellRad,biggestRad)

			#Grow each garnet with composition nextShellCompo and thickness of shellThick
			for i in range(len(self.garnetList)):

				self.garnetList[i] = self.garnetList[i].growGarnet(nextShellCompo, self.shellThick)

			#Check if new garnet needs to be nucleated
			if(len(self.crystalList) > len(self.garnetList)):
				#Nucleation threshold is the difference in radius between the last garnet and the next garnet
				#For ellipsoids, uses the a-axis
				nucThresh = self.crystalList[len(self.garnetList)-1].getDim()-self.crystalList[len(self.garnetList)].getDim()


				#Check if the youngest garnet is big enough to justify nucleation of a new garnet
				if self.garnetList[len(self.garnetList)-1].bigAx >= nucThresh:

					self.nucleateGarnet(self.crystalList[len(self.garnetList)],nextShellCompo)



	def getShellCompo(self,xHi,xLo):
		#Gets the average composition of the profile between xHi and xLo and returns it
		#As a list of GarnetComponentMols
		shellCompo = []

		for i in range(len(self.grtProfile.interpComp)):
			thisProfile = self.grtProfile.interpComp[i]
			if(xHi <= self.crystalList[0].getDim()):
				shellX = (thisProfile(xHi) + thisProfile(xLo))/2
			else:
				shellX = (thisProfile(self.crystalList[0].getDim()) + thisProfile(xLo))/2
			shellCompo.append(GarnetComponentMol(GRT_CMPNT[i],shellX))
		return shellCompo



	def nucleateGarnet(self, garnetShape,garnetCompo):
		#Function to nucleate a new garnet with the same aspect ratio of garnet shape

		rescaleFactor = garnetShape.getDim()/self.shellThick #Determines the scaling factor required to maintain the aspect ratio of a garnet with dimension of shell thickness

		nucleusShape = garnetShape.getRescale(rescaleFactor)

		nucleus = Garnet(nucleusShape, garnetCompo)
		self.garnetList.append(nucleus)



	def calcTotalGarnetMol(self):
		#Calculate total mols of all garnet components
		#This will return an array of ComponentMol not GarnetComponentMol
		self.totGarnetMol = self.garnetList[0].getCompoAsComponentMol() #Get the composition of the first garnet


		for i in range(1,len(self.garnetList)):
			#Add each garnet composition to totGarnetMol

			thisGarnetCompo = self.garnetList[i].getCompoAsComponentMol()
			self.totGarnetMol = addComponentList(self.totGarnetMol,thisGarnetCompo)
			



	def writeScriptFiles(self, thisDir, fracStep, database):
		#Write script files for the current composition
		#For isopleths, it uses the composition of the next biggest shell

		#First get the composition of the next shell, this is what will be written into the script file
		biggestRad = self.garnetList[0].bigAx
		nextShellRad = biggestRad + self.shellThick

		nextShellCompo = self.getShellCompo(nextShellRad,biggestRad)
		currComposition = subComponentList(self.composition, self.totGarnetMol)

		# print("Total Composition:")
		# compoString = ""
		# for cmpnt in self.composition:
		# 	compoString += cmpnt.element +": " + str(cmpnt.mol) + ", "
		# print(compoString)
		# compoString = ""
		# print("After removal of garnet:")
		# for cmpnt in currComposition:
		# 	compoString += cmpnt.element +": " + str(cmpnt.mol) + ", "
		# print(compoString)

		iterName = self.name + '_Stage{:02d}'.format(fracStep)
		#Generate the therin composition string
		therin = ""
		for i in range(len(currComposition)):
			if currComposition[i].mol < 0:
				currComposition[i].mol = 0
			therin += currComposition[i].element.upper() + "({:7.6f})".format(currComposition[i].mol)

		phaseScript(therin,P1,P2,T1,T2,iterName,thisDir,database)

		#Now generate the isopleth script files
		for i in range(len(nextShellCompo)):
			componentName = nextShellCompo[i].endMember
			targetCompo = nextShellCompo[i].molFrac
			#Calculate range of mol fraction +- 10% of the target composition
			compoStep = round_sig(targetCompo*0.05)
			compoStart = round_sig(targetCompo - 2*compoStep)
			compoEnd =round_sig( targetCompo + 2*compoStep)
			isoScript(therin, P1, P2, T1, T2, iterName, thisDir, database,"GARNET", componentName,compoStart, compoEnd,compoStep)

	def getAvgEllipsoid(self, blobIn):
		#Takes the blobIn as a pandas table
		#Average the aspect ratios of all the ellipsoids and returns the average ellipsoid
		#This way we can work with a "standardized" ellipsoid that grows the same way for every garnet
		rad1 = blobIn['PEllipsoid Rad1 (mm)'].to_numpy()
		rad2 = blobIn['PEllipsoid Rad2 (mm)'].to_numpy()
		rad3 = blobIn['PEllipsoid Rad3 (mm)'].to_numpy()

		#ratio12 = rad1/rad2 ratio23 = rad2/rad3 ratio12*ratio23 = rad1/rad3
		ratio12 = rad1/rad2
		ratio23 = rad2/rad3

		avgR12 = np.average(ratio12)
		avgR23 = np.average(ratio23)

		#Volume of ellipsoid doesnt matter so set rad3 = 1
		modelR2 = avgR23
		modelR1 = avgR12*modelR2
		modelEllip = Ellipsoid(modelR1,modelR2,1)

		return modelEllip



		



def round_sig(x, sig=3):
   	return round(x, sig-int(math.floor(math.log10(abs(x))))-1)





