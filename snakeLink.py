class LINK:
    def __init__(self, linkName, pos, size, sensorYN):
        self.linkName = str(linkName)
        self.pos = pos
        self.size = size
        self.sensorYN = sensorYN
    
    def Get_Front_Joint_Pos(self):
        self.frontCenter = self.pos
        self.frontCenter[0] = self.pos[0]+(self.size[0]/2)

        return self.frontCenter