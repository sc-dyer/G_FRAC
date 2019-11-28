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
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import easygui
import math
import copy

NUM_SHELLS = 2000 #This is the number of garnet shells the biggest garnet will have 

class GarnetCSD:

	def __init__(self,blobFileName,garnetProfile,rockCompo, rockVolume):

		self.composition = rockCompo #This is a list of ComponentMol objects that define the rock composition
		self.grtProfile = garnetProfile #This is the CompoProfile object that is a half profile that defines the zoning in the garnet
		self.rockVol = rockVolume
		#Now need to open up the blob file to build the crystal list
		blobDF = pd.read_excel(blobFileName) #Assumes that formatting has not changed from default blob output

		self.crystalList = [] #Empty list to fill with Shape entries

		#Ask user to choose if using spheres or ellipsoids
		msg = "Are garnets spheres or ellipsoids?"
		title = ""
		choices = ["Sphere","Ellipsoid"]
		#reply = easygui.buttonbox(msg,title,choices)
		reply = "Sphere" #Only works for Spheres right now, need to think about size independent growth of ellipsoids
		if(reply==choices[0]):
			volume = list(blobDF['Volume (mm^3)'])

			for i in range(len(volume)):
				#If spheres, it will recalculate the radius from the volume
				if not math.isnan(volume[i]):
					thisRad = (volume[i]*3/(4*math.pi))**(1./3)
					self.crystalList.append(Sphere(thisRad))

		elif(reply == choices[1]):
			#If ellipsoid it uses the PEllipsoid data
			#It should be that rad1 > rad2 > rad3
			rad1 = list(blobDF['PEllipsoid Rad1 (mm)'])
			rad2 = list(blobDF['PEllipsoid Rad2 (mm)'])
			rad3 = list(blobDF['PEllipsoid Rad3 (mm)'])

			for i in range(len(rad1)):
				if not math.isnan(rad1[i]):
					self.crystalList.append(Ellipsoid(rad1[i],rad2[i],rad3[i]))
		else:
			print("Error: No option chosen")
			return

		#Okay now we need to stretch the garnet profile to fit with the long dimension of the ellipsoid or the radius of the sphere
		
		
		self.quickSortCrystals(0,len(self.crystalList)-1)
		travRad = max(self.grtProfile.x) #Radius of the garnet measured in the microprobe profile
		scaleFactor = self.crystalList[0].getDim()/travRad #The scaling factor to convert the x values in grtProfile to be the same size as the radius or a axis of ellipsoid

		self.shellThick = self.crystalList[0].getDim()/NUM_SHELLS #Thickness of each shell
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

	def fractionateGarnet(self, radInterval):
		#A method to fractionate garnet and output the composition at each radInterval
		count = 1
		self.growGarnetShell()
		while(self.garnetList[0].bigAx < self.crystalList[0].getDim()-self.shellThick):
			#Grow garnet until the biggest garnet is one shell away from its max size
			self.growGarnetShell()
			
			if(abs(self.garnetList[0].bigAx-radInterval*count)<self.shellThick):
				count += 1
				print("Biggest Radius = " + str(self.garnetList[0].bigAx))
				print(self.garnetList[0].composition[0].endMember + ": " + str(self.garnetList[0].composition[0].molFrac))
				print("Number of garnets: " + str(len(self.garnetList)))
				self.calcTotalGarnetMol()
				for i in range(len(self.totGarnetMol)):
					print("Total mol of " + self.totGarnetMol[i].element + " = " + str(self.totGarnetMol[i].mol))
				

		print("One more iteration: " + str(self.crystalList[0].getDim()))

	def growGarnetShell(self):
		#Function to grow an additional shell of garnet
		#Will add a new garnet once the radius difference between the last garnet and the next one is sufficient

		if len(self.garnetList) == 0: #Initialize first garnet
			firstShellCompo = self.getShellCompo(self.shellThick,0)
			self.nucleateGarnet(self.crystalList[0],firstShellCompo)
			print("Nucleating first garnet")
		else:
			#First calculate the next composition interval
			biggestRad = self.garnetList[0].bigAx
			nextShellRad = biggestRad + self.shellThick
			nextShellCompo = self.getShellCompo(nextShellRad,biggestRad)

			#print("Next Shell Rad:" + str(nextShellRad))
			#print("Next Shell " + nextShellCompo[0].endMember + ": " + str(nextShellCompo[0].molFrac))

			#Grow each garnet with composition nextShellCompo and thickness of shellThick
			for i in range(len(self.garnetList)):

				self.garnetList[i] = self.garnetList[i].growGarnet(nextShellCompo, self.shellThick)

			#Check if new garnet needs to be nucleated
			if(len(self.crystalList) > len(self.garnetList)):
				nucThresh = self.crystalList[len(self.garnetList)-1].getDim()-self.crystalList[len(self.garnetList)].getDim()

				#print("Nucleation thershold: " + str(nucThresh))

				#Check if the youngest garnet is big enough to justify nucleation of a new garnet
				if self.garnetList[len(self.garnetList)-1].bigAx >= nucThresh:

					#print("Smallest Garnet Radius: " + str(self.garnetList[len(self.garnetList)-1].bigAx))

					self.nucleateGarnet(self.crystalList[len(self.garnetList)],nextShellCompo)

	def getShellCompo(self,xHi,xLo):
		#Gets the average composition of the profile between xHi and xLo and returns it
		#As a list of GarnetComponentMols
		shellCompo = []

		for i in range(len(self.grtProfile.interpComp)):
			thisProfile = self.grtProfile.interpComp[i]
			
			shellX = (thisProfile(xHi) + thisProfile(xLo))/2
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
			

	#def writeScriptFiles(self):

