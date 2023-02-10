class LINK:
    def __init__(self, linkName, pos, size):
        self.linkName = str(linkName)
        self.pos = pos
        self.size = size
    
    def Get_Back_Joint_Pos(self):
        self.backCorner = self.pos
        self.backCorner[0] = self.pos[0]-(self.size[0]/2)