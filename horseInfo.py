import random as rd
import numpy as np

from snakeLink import LINK
from snakeJoint import JOINT

class HORSE_INFO:
    def __init__(self, numLinks, origin):
        self.numLinks = numLinks
        self.origin = origin
        self.links = {}
        self.joints = {}
        self.linksize = np.random.uniform(low=0.25, high=0.75, size=(self.numLinks, 3))
    
    def Choose_Propagation_Axis(self):
        self.propAxis = np.random.randint(low=0, high=3, size=self.numLinks)
        
        self.add_vec = np.zeros((self.numLinks, 3))
        for link in range(self.numLinks):
            for dim in range(3):
                if self.propAxis[link] == dim:
                    self.add_vec[link][dim] = self.linksize[link][dim]/2
        
        return self.add_vec

    def Get_Joints_and_Links(self):
        self.Choose_Propagation_Axis()

        self.links[0] = LINK(linkName = 0,
                            pos = self.origin, 
                            size = self.linksize[0], 
                            sensorYN = rd.randint(0,1))
        self.joints[0] = JOINT(jointName = "0_1", 
                               parentLink = "0", 
                               childLink = "1", 
                               jointPos = self.origin + self.add_vec[0],
                               jointAxis = self.Get_Joint_Axis(rd.randint(0,1)))

        for linkIndex in range(1, self.numLinks):
            self.links[linkIndex] = LINK(linkName = linkIndex, 
                                    pos = self.add_vec[linkIndex]/2, 
                                    size = self.linksize[linkIndex],
                                    sensorYN = rd.randint(0,1))
            if linkIndex < self.numLinks-1:
                parentLink = str(linkIndex)
                childLink = str(linkIndex+1)
                jointName = parentLink+"_"+childLink
                self.joints[linkIndex] = JOINT(jointName = jointName, 
                                        parentLink = parentLink, 
                                        childLink = childLink, 
                                        jointPos = self.add_vec[linkIndex]*2,
                                        jointAxis = self.Get_Joint_Axis(rd.randint(0,1)))
        
        return self.links, self.joints
    
    def Get_Joint_Axis(self, jointAxisCode):
        if jointAxisCode == 0:
            jointAxis = "0 1 0"
        else:
            jointAxis = "0 0 1"
        return jointAxis