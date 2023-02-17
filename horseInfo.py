import random as rd
import numpy as np

from snakeLink import LINK
from snakeJoint import JOINT

class HORSE_INFO:
    def __init__(self, numLinks, origin):
        self.numLinks = numLinks
        self.numJoints = self.numLinks - 1
        self.origin = origin
        self.links = {}
        self.joints = {}
        self.linksize = np.random.uniform(low=0.25, high=0.75, size=(self.numLinks, 3))

    def Choose_Propagation_Stream(self):
        self.propAxis = np.random.randint(low=0, high=3, size=self.numJoints)
    
        self.relLinkPos = np.zeros((self.numLinks, 3))
        for link in range(1, self.numLinks):
            self.relLinkPos[link][self.propAxis[link-1]] = self.linksize[link][self.propAxis[link-1]]/2
        
        self.relJointPos = np.zeros((self.numJoints, 3))
        self.relJointPos[0][self.propAxis[0]] = self.linksize[0][self.propAxis[0]]/2
        for joint in range(1, self.numJoints):
            if self.propAxis[joint] == self.propAxis[joint-1]:
                self.relJointPos[joint][self.propAxis[joint]] = self.linksize[joint][self.propAxis[joint]]
            else:
                self.relJointPos[joint][self.propAxis[joint-1]] = self.linksize[joint][self.propAxis[joint-1]]/2
                self.relJointPos[joint][self.propAxis[joint]] = self.linksize[joint][self.propAxis[joint]]/2

    def Get_Joints_and_Links(self):
        self.Choose_Propagation_Stream()

        self.links[0] = LINK(linkName = 0,
                            pos = self.origin, 
                            size = self.linksize[0], 
                            sensorYN = rd.randint(0,1))
        self.joints[0] = JOINT(jointName = "0_1", 
                               parentLink = "0", 
                               childLink = "1",
                               jointType = "revolute",
                               jointPos = self.origin + self.relJointPos[0],
                               jointAxis = self.Get_Joint_Axis(self.propAxis[0], rd.randint(0,1)))

        for linkIndex in range(1, self.numLinks):
            self.links[linkIndex] = LINK(linkName = linkIndex, 
                                        pos = self.relLinkPos[linkIndex],
                                        size = self.linksize[linkIndex],
                                        sensorYN = rd.randint(0,1))
            if linkIndex < self.numLinks-1:
                parentLink = str(linkIndex)
                childLink = str(linkIndex+1)
                jointName = parentLink+"_"+childLink
                self.joints[linkIndex] = JOINT(jointName = jointName, 
                                                parentLink = parentLink, 
                                                childLink = childLink,
                                                jointType = "revolute",
                                                jointPos = self.relJointPos[linkIndex],
                                                jointAxis = self.Get_Joint_Axis(self.propAxis[linkIndex], rd.randint(0, 1)))
        
        return self.links, self.joints
    
    def Get_Joint_Axis(self, propAxis, randBit):
        if propAxis == 0:
            if randBit == 0:
                jointAxis = "0 1 0"
            else:
                jointAxis = "0 0 1"
        elif propAxis == 1:
            if randBit == 0:
                jointAxis = "1 0 0"
            else:
                jointAxis = "0 0 1"
        else:
            if randBit == 0:
                jointAxis = "0 1 0"
            else:
                jointAxis = "1 0 0"
        
        return jointAxis