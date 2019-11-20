#Abstract class definition of a shape
#Garnets can have a shape (sphere or ellipsoid)
#All shapes have volume and surface area but I am excluding SA for now

from abc import ABC, abstractmethod 

class Shape(ABC):

	def getVolume():
		pass

	def calcVol():
		pass