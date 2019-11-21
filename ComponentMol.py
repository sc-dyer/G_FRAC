#This is a simple class for monitoring concentration of a component in a rock or mineral composition
from Component import Component
import copy

class ComponentMol(Component):

	def __init__(self, componentIn, molIn=0):
		#Initialize the super using the parameters of componentIn
		super().__init__(componentIn.element, componentIn.weight, componentIn.ox2cat, componentIn.catNum)
		if(molIn !=0):
			self.mol = molIn
