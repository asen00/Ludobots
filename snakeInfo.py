import numpy as np

from snakeLink import LINK
from snakeJoint import JOINT

class SNAKE_INFO: 
    def __init__(self, numLinks):
        self.numLinks = numLinks
        self.links = {}
        self.joints = {}

    def Get_Links(self):
        self.links[0] = LINK("0", [0,0,0], np.random.randint(low=0, high=11, size=3))

        for linkName in range(1, self.numLinks):
            self.links[linkName] = LINK(linkName, np.random.randint(low=0, high=11, size=3), np.random.randint(low=0, high=11, size=3))
        
        return self.links

    def Get_Joints(self):
        for i in range(self.numLinks-1):
            parentLink = str(i)
            childLink = str(i+1)
            jointName = parentLink+"_"+childLink
            jointPos = self.links[i].Get_Back_Joint_Pos()
            jointAxisVec = np.random.randint(low=0, high=2, size=3)

            jointAxis = ""
            for i in range(3):
                jointAxis += str(jointAxisVec[i])+" "

            self.joints[i] = JOINT(jointName, parentLink, childLink, jointPos, jointAxis)
        
        print(self.joints)
        return self.joints