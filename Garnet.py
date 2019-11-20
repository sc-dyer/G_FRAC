#This is a garnet
#I am going to attempt to define it recursively
#God help me

#Garnets have a shape, composition, and density
from Shape import Shape 
from Geochem_const import *
from Component import Component

class Garnet:

	#Base case, the base shape should have the same dimensions of the shell thickness
	#E.g if shell thickness is 0.002 then the radius of the basecase sphere should be 0.002
	#I guess for ellipsoids since shell thickness varies depending on the axis we will define shell thickness as the one used for the a axis
	def __init__(self,crystalShape,grtCompo,nextGarnet=None):
		self.grtShape = crystalShape
		self.shellThick = self.grtShape.getDim()#Gets radius for sphere and aAx for ellipsoid
		self.composition = grtCompo #Assume array in form CMPNT
		self.density = GRT_DENSITY #Assumes same density for all (just for now I guess)

		self.nextShell = nextGarnet #base case is None, the next garnet can have its own composition and density


		self.totVol = self.grtShape.getVolume() #Total volume is same as shape volume
		if(nextGarnet != None):
			self.shellVol = self.totVol - self.nextShell.totVol #Shell volume is the total volume less total volume of the next smallest shell
		else:
			self.shellVol = self.totVol #Base case tot and shell vol are same
		#Get the mols of the shell and the mols of the garnet
		self.calcShellMol() 
		self.calcTotMol()




	def calcShellMol(self):
		#This will calculate the mols of components in a single shell in this garnet
		#Assumes that the form of garnet is X3Al2Si3O12 where X is anything in CMPNT
		#Will also renormalize composition to 1 in case there are minor discrepencies
		mass = self.shellVol*self.density #Calculated mass of garnet
		molGrt = []

		for i in range(len(self.composition)):
			#Calculate mols of garnet for each component
			massSum = 0
			for j in range(len(self.composition)):
				#Sum up the masses of each component based on mol fraction
				massSum += self.composition[j]*GRT_M[j]

			cmpntMol = self.composition[i]*mass/massSum #Convert the mol fraction to mols
			molGrt.append(cmpntMol)

		self.shellMol = molGrt

	def calcTotMol(self):
		#Not a truly recursive function but close enough
		#Trying to limit our coputation time and ram usage
		if(self.nextShell == None):
			#Define the basecase where only one shell so total mol is shellMol
			self.totMol = self.shellMol
		else:
			self.totMol = []
			for i in range(len(self.shellMol)):
				self.totMol.append(self.nextShell.totMol[i]+self.shellMol[i])#Takes total from the next shell and adds it to current shell
			