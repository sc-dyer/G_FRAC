#Its a sphere
#A possible shape for a garnet
#Has a volume and a radius
#I probably could have made this a special instance of ellipsoid but its too late I already committed
from Shape import Shape
import math

class Sphere(Shape):

	def __init__(self,rad):
		self.radius = rad
		self.calcVol()

	def calcVol(self):
		#Calculates the volume of the sphere
		vol = 4/3*math.pi*self.radius**3
		self.volume = vol

	def getVolume(self):
		return self.volume

	def getDim(self):
		return self.radius

	def growByDim(self, dim):
		#Increment radius by dim
		self.radius += dim
		self.calcVol()

	def calcRad(self):
		#working backwards to get radius from volume
		rad = (self.volume*3/(4*math.pi))**(1./3)
		self.radius = rad

	def growByVol(self, vol):
		#Increment volume by vol
		self.volume += vol
		self.calcRad()