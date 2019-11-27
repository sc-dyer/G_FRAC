#This is like ComponentMol but instead its for the GarnetComponents
#There is probably a more polymorphic way to implement these but this works for now
#By for now I mean forever
from GarnetComponent import GarnetComponent

class GarnetComponentMol(GarnetComponent):

	def __init__(self,grtIn, xIn=0, molIn=0):
		#Takes all properties from grtIn and assigns an amount of mols and a mol fraction
		super().__init__(grtIn.cation,grtIn.endMember,grtIn.formula)
		self.molFrac = xIn #This should add to 1 with the other garnet components
		self.mol = molIn

	def getComponentMols(self):
		#Method that returns a list of ComponentMols which make up the GarnetComponentMol
		componentList = []

		for i in range(len(self.formula)):
			#For each component in the formula, multiply it by the mol of the garnetComponent
			mol = self.formula[i].mol*self.mol
			compenentList.append(ComponentMol(formula[i],mol))

		return componentList
