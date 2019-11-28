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
	matchIndex2 = []
	for i in range(len(cList1)):
		#cycle through cList1 and try to add every component from cList2
		didMatch = False
		for j in range(len(cList2)):
			molSum = cList1[i].sumComponents(cList2[j])
			#Check to see if molSum was calculated
			if molSum != None:

				summedList.append(molSum)
				#If molSum calculated then keep track of the index in list 2 
				#print("They match")
				didMatch = True
				matchIndex2.append(j)

		if not didMatch:
			summedList.append(cList1[i])

	#Only append the components that didnt have a match in the second list
	for i in range(len(cList2)):
		#Saves if it has a match in matchIndex2
		noMatch = True
		for j in range(len(matchIndex2)):
			if i == matchIndex2[j]:
				noMatch = False
		if noMatch:
			summedList.append(cList2[i])
	
	return summedList