#General class to be extended by the Traverse class and the Model class
#Defines methods that can be used by any garnet composition profile
#Extended by Model and Traverse
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
from GeochemConst import GRT_CMPNT
from scipy.interpolate import interp1d

class CompoProfile:

	def __init__(self):

		#Empty initialization, defines the variables all CompoProfiles should have

		self.x = [] #distance in mm
		#mol fraction
		self.pltColour = 'black'
		self.pltLine = 'None'
		self.pltMark = 'None'
		self.cmpnts = [[],[],[],[]]#Array for mn,mg,ca,fe, each corresponds to a value in CMPNT
		


	def plotCompo(self, key, pltIn,mrkSize):
		#Plots the composition of a specific component in pltIn
		#input key should be one of the CMPNT
		#mrkSize input used for convenience when plotting things on different sized plots
		for i in range(len(GRT_CMPNT)):
			if(key==GRT_CMPNT[i].cation):
				yComp = self.cmpnts[i]
			
		
		pltIn.plot(self.x, yComp, color = self.pltColour, marker = self.pltMark, linestyle = self.pltLine, markersize = mrkSize, linewidth = 1, label = key)
	
	def getCmpnt(self, key):
		#Returns the array of whatever component was input to key
		#This is for user probing
		val = []
		for i in range(len(GRT_CMPNT)):
			if(key==GRT_CMPNT[i].cation):
				val = self.cmpnts[i]
		return val

	def compareProfile(self,compare,wFile, name):
		#Comparison must be another CompoProfile object
		#This method returns multiple values of S (standard error) for each component in the form of Root Mean Squared Error, plus an average value of S. 
		#The unit of S is mol fraction, 
		#Assumes that these are two non-identical arrays CompoProfiles (e.g. a model and a traverse, or two different models)
		#Also assumes that both arrays start from core and go to the rims, does not perform any translations 
		#Will take each x value of comparison and find what the composition should be at that x in "this"
		#Does this by interpolating between the closest two points at each x in compare
		#The intention is to compare a model profile to a half traverse, so it will interpolate values between points on the model for a least square regression

		self.rmse= [] #Standard Error as root mean square error
		self.nrmse = [] #Normalized RMSE
		
		for i in range(len(GRT_CMPNT)):
			thisCmpnt = []
			thatCmpnt = []
			

			for j in range(len(compare.x)):
				compoAtX = self.interpCompoAtX(compare.x[j],GRT_CMPNT[i].cation)
				if compoAtX >= 0:
					thisCmpnt.append(compoAtX)
					thatCmpnt.append(compare.cmpnts[i][j])

			thisCmpnt = np.array(thisCmpnt)
			thatCmpnt = np.array(thatCmpnt)
			rmse = np.sqrt(((thisCmpnt - thatCmpnt)**2).mean()) #calculate root mean square error
			
			nrmse = rmse/(thatCmpnt.mean()) #Normalize to mean of the measured profile, NOTE: Can also use the range -> try both?

			self.rmse.append(rmse)
			self.nrmse.append(nrmse)
		
		#Build next line to write to file in the order of RMSE(CMPNT1),RMSE(CMPNT2)...,RMSE(Average),NRMSE(CMPNT1),NRMSE(CMPNT2)..NRMSE(Average)
		nextLine = name + ","
		for i in range(len(self.rmse)):
			nextLine += str(self.rmse[i]) + ","
		nextLine += str(sum(self.rmse)/len(self.rmse)) + ','

		for i in range(len(self.nrmse)):
			nextLine += str(self.nrmse[i]) + ","
		nrmseAvg = sum(self.nrmse)/len(self.nrmse)
		nextLine += str(nrmseAvg) + '\n'

		

		wFile.write(nextLine)

		return nrmseAvg
		
			
	def interpCompoAtX(self,xVal,key):
		#Linearly interpolate the composition between to points on the model to get the exact value at an x position

		count = 0
		while count < len(self.x) and self.x[count] < xVal:
					count += 1

		compoAtX = -1 
		if count >= 0 and count <len(self.x):
			for i in range(len(GRT_CMPNT)):

				if GRT_CMPNT[i].cation == key:
					rightX = self.x[count]

					leftX = self.x[count-1]
				
					rightCmpnt = self.cmpnts[i][count]
					leftCmpnt = self.cmpnts[i][count-1]

					#linearly interpolate between two points and get the value at xVal
					slope = (rightCmpnt-leftCmpnt)/(rightX-leftX)
					midX = xVal - leftX
					compoAtX = midX*slope + leftCmpnt

		return compoAtX #Returns -1 if the first cell was to the right of the input xVal or if it is attempting to interpolate past the model size


	def scipyInterp(self, kindIn='linear'):
		#Function that initializes numpy arrays for each component and interpolates the values to create continuous functions
		#
		npCmpnts = np.array([np.array(cmpnt) for cmpnt in self.cmpnts]) #Make numpy arrays for each component
		npX = np.array(self.x)
		self.interpComp = []
		#Interpolate each component with npX and store new function in interpComp
		for i in range(len(npCmpnts)):
			thisInterp = interp1d(npX, npCmpnts[i],kind=kindIn)
			self.interpComp.append(thisInterp)


