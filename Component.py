#A simple class to define elemental components of a rock
class Component:
    
    def __init__(self):
        self.element = None
        self.weight = 0
        self.ox2cat = 0 #ratio of O to cation
        self.catNum = 0
        
    def __init__(self, name, M, ox, cNum, cat):
        
        self.element = name
        self.weight = M
        self.ox2cat = ox #ratio of O to cation if in an oxide
        self.catNum = cNum # Num of cations in an oxide
        
        