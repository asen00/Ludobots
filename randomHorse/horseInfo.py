import random as rd
import numpy as np

from randomSnake.snakeLink import LINK
from randomSnake.snakeJoint import JOINT

class HORSE_INFO:
    def __init__(self, numLinks, origin):
        self.numLinks = numLinks
        self.origin = origin
        self.links = {}
        self.joints = {}
        self.linkXsize = np.random.random(size=self.numLinks)*rd.random()+rd.random()
    
    def Get_Joints_and_Links(self):
        self.links[0] = LINK(linkName = 0, 
                            pos = self.origin, 
                            size = [self.linkXsize[0], rd.random()*rd.random()+rd.random(), rd.random()*rd.random()+rd.random()], 
                            sensorYN = rd.randint(0,1))
        self.joints[0] = JOINT(jointName = "0_1", 
                               parentLink = "0", 
                               childLink = "1", 
                               jointPos = [self.origin[0]+self.linkXsize[0]/2, self.origin[1], self.origin[2]], 
                               jointAxis = self.Get_Joint_Axis(rd.randint(0,1)))

        for i in range(1, self.numLinks):
            self.links[i] = LINK(linkName = i, 
                                    pos = [self.linkXsize[i]/2, 0, 0], 
                                    size = [self.linkXsize[i], rd.random()*rd.random()+rd.random(), rd.random()*rd.random()+rd.random()],
                                    sensorYN = rd.randint(0,1))
            if i < self.numLinks-1:
                parentLink = str(i)
                childLink = str(i+1)
                jointName = parentLink+"_"+childLink
                self.joints[i] = JOINT(jointName = jointName, 
                                        parentLink = parentLink, 
                                        childLink = childLink, 
                                        jointPos = [self.linkXsize[i], 0, 0], 
                                        jointAxis = self.Get_Joint_Axis(rd.randint(0,1)))
        
        return self.links, self.joints
    
    def Get_Joint_Axis(self, jointAxisCode):
        if jointAxisCode == 0:
            jointAxis = "0 1 0"
        else:
            jointAxis = "0 0 1"
        return jointAxis