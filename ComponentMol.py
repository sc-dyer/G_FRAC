#This is a simple class for monitoring concentration of a component in a rock or mineral composition
from Component import Component
import copy

class ComponentMol(Component):

	def __init__(self, componentIn, molIn=0):
		#Initialize the super using the parameters of componentIn
		super().__init__(componentIn.element, componentIn.weight, componentIn.ox2cat, componentIn.catNum)
		
		self.mol = molIn
		
	def sumComponents(self,otherComp):
		#Returns a new component that is a sum of the two
		#Checks if it is the same type of component

		if(self.element == otherComp.element):
			summedMol = self.mol + otherComp.mol
			return ComponentMol(self,summedMol)
		#returns nothing if they dont match


def addComponentList(cList1, cList2):
	#This is a function to add together the composition of cList1 and cList2
	#Returns another list of componentmols
	summedList = []
	for i in range(len(cList1)):
		#cycle through cList1 and try to add every component from cList2
		for j in range(len(clist2)):
			summedList.append(cList1[i].sumComponents(cList2[j]))
	
	return summedList