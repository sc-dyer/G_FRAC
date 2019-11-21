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

class GarnetCSD:

	def __init__(self,blobFileName,garnetProfile):