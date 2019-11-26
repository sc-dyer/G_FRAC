#This is a class for reading and modelling garnet CSDs
#It can read a blob output file and use Garnet.py to model garnet growth
#Maybe it will do more in the far future but this is the goal for now

from Garnet import Garnet
from GeochemConst import *
from Shape import Shape
from Sphere import Sphere
from Ellipsoid import Ellipsoid
from CompoProfile import CompoProfile
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import easygui
import math

class GarnetCSD:

	def __init__(self,blobFileName,garnetProfile,rockCompo):

		self.composition = rockCompo #This is a list of ComponentMol objects that define the rock composition
		self.grtProfile = garnetProfile #This is the CompoProfile object that is a half profile that defines the zoning in the garnet

		#Now need to open up the blob file to build the crystal list
		blobDF = pd.read_excel(blobFileName, sheetname = "Sheet1") #Assumes that formatting has not changed from default blob output

		self.crystalList = [] #Empty list to fill with Shape entries

		#Ask user to choose if using spheres or ellipsoids
		msg = "Are garnets spheres or ellipsoids?"
		title = ""
		choices = ["Sphere","Ellipsoid"]
		reply = easygui.buttonbox(msg,title,choices)

		if(reply==choices[0]):
			volume = list(blobDF['Volume (mm^3)'])

			for i in range(len(volume)):
				#If spheres, it will recalculate the radius from the volume
				thisRad = (volume[i]*3/(4*math.pi))**(1./3)
				self.crystaList.append(Sphere(thisRad))

		else if(reply == choices[1]):
			#If ellipsoid it uses the PEllipsoid data
			#It should be that rad1 > rad2 > rad3
			rad1 = list(blobDF['PEllipsoid Rad1 (mm)'])
			rad2 = list(blobDF['PEllipsoid Rad2 (mm)'])
			rad3 = list(blobDF['PEllipsoid Rad3 (mm)'])

			for i in range(len(rad1)):
				self.crystalList.append(Ellipsoid(rad1,rad2,rad3))
		else:
			print("Error: No option chosen")
			return

