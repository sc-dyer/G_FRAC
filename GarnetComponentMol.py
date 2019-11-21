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
