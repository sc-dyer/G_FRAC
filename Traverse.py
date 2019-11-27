#Class to open and manage the measured garnet traverse
#Must be in a csv file with the following header:
#x (mm),Ca,Mg,Fe,Mn 
#The unit for components should be mol fraction
#This class is an extension of CompoProfile
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import easygui

from CompoProfile import CompoProfile
from GeochemConst import GRT_CMPNT, ALM

class Traverse(CompoProfile):

	def __init__(self, fileName):
		#Read the file containg probe data and store it in this object

		CompoProfile.__init__(self)
		self.pltMark = 'o'

		#open the csv file
		try:
			grtFile = open(fileName, 'r')
		except:
			print("No csv file found at location:")
			print(fileName)
			return
		
		grtdf = pd.read_csv(fileName)
		self.x = list(grtdf['x (mm)'])
		for i in range(len(GRT_CMPNT)):
			self.cmpnts[i] = list(grtdf[GRT_CMPNT[i].cation])

		

	def plotAll(self, pltIn):
		#Method to plot all components on one plot
		#Assumes that the Fe component is much higher than the rest, plots it on seperate axis
		colours = ['green','blue','orange','red']
		symbols = ['o','^','s','P']
		pltAlm = pltIn.twinx()
		
		self.travPlot = pltIn #Saves the plot to the object

		#Loop for plotting
		for i in range(len(GRT_CMPNT)):
			self.pltColour = colours[i]
			self.pltMark = symbols[i]
			if(GRT_CMPNT[i] == ALM):
				CompoProfile.plotCompo(self,GRT_CMPNT[i].cation,pltAlm,7)
			else:
				CompoProfile.plotCompo(self,GRT_CMPNT[i].cation,pltIn,7)

		pltIn.set_xlabel("x (mm)")
		pltIn.set_ylabel("X (Ca,Mn,Mg)")

		#Uncomment these lines if you want everything on the same scale
		#pltIn.set_ylim(0,0.4)
		#pltAlm.set_ylim(0.45,0.85)

		pltAlm.set_ylabel("X (Fe)")
		pltIn.legend(fontsize = 14, loc = 'upper left')
		pltAlm.legend(fontsize = 14, loc = 'upper right')

		#This is to set up the stuff for splitting the plot in half, assuming that you input a full traverse instead of a half traverse
		self.cid = pltIn.figure.canvas.mpl_connect('button_press_event',self.travClick)
		self.splitLine = pltIn.plot([0],[0]) #create an empty line
		self.selectedTrav = self.splitTrav(self.x[0] - 1,False)#Sets the baseline to leftTrav is empty and rightTrav = this. This is basically if you want to input just a half traverse, however it assumes that it is the right half

	def travClick(self, event):
		#When the plot is clicked, draw a vertical line where clicked and store that value as the new 0 for splitting the traverse
		#Will ask for confirmation before drawing and storing the location.
		#It can be changed as many times as desired
		self.splitLine.pop(0).remove()
		newZero = event.xdata
		self.travPlot.autoscale(False)
		self.splitLine = self.travPlot.plot([newZero,newZero],[-100,100],color = 'black',linestyle = '--')
		
		
		title = ""
		msg = "Split traverse at x = " + str(newZero) + "?"
		answer = easygui.boolbox(msg,title,["Yes","No"])
		#answer = input('Split traverse at x = ' + str(newZero) +'? (y/n)')
		if answer:
			msg = "Take the left or right side?"
			selLeft = easygui.boolbox(msg,title,["Left","Right"])
			self.selectedTrav = self.splitTrav(newZero,selLeft)
			plt.draw()
			print("Done, you may now exit this plot or choose a different x location to split the traverse.")

		

	def splitTrav(self,xPos, selectLeft):
		#Method for splitting the traverse into two halves at the inputted xPos
		#Assumes xpos will never exactly equal to an x position on the traverse
		#The two halves are CompoProfile objects with the same data of their respective halves of this Traverse object
		#They will be stored in the travSplit array so that they can be ambiguously referenced. 
		#They will contain a little less info but maintain most of the core stuff

		count = 0
		#Finds the index of the datapoint to the right of the selected x
		while(self.x[count] < xPos):
			count+=1


		xRightIndex = count

		xLeftIndex = count - 1
	
		#initialize travSplit array to hold the two halves and the two sides of the traverse
		self.travSplit= []
		rightTrav = CompoProfile()
		leftTrav = CompoProfile()
		rightTrav.pltMark = 'o'
		leftTrav.pltMark = 'o'
		leftTrav.pltColour = 'blue' #So it can be differentiated on the plot

		#Build the contained arrays
		for i in range(xRightIndex,len(self.x)):
			
			rightTrav.x.append(self.x[i] - xPos)
			for j in range(len(GRT_CMPNT)):
				rightTrav.cmpnts[j].append(self.cmpnts[j][i])
			

		#Flips the left Traverse
		for i in range(xLeftIndex,-1,-1):
			leftTrav.x.append(xPos - self.x[i])
			for j in range(len(GRT_CMPNT)):
				leftTrav.cmpnts[j].append(self.cmpnts[j][i])


		#Add the two traverses to travSplit
		if len(rightTrav.x) > 0:
			self.travSplit.append(rightTrav)
			if not selectLeft:
				return rightTrav
		if len(leftTrav.x) > 0:
			self.travSplit.append(leftTrav)
			if selectLeft:
				return leftTrav
	



