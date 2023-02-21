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

    def Choose_Link_Sizes(self, numLinks):
        snakeLinkSizes = np.random.uniform(low=0.25, high=0.75, size=(numLinks, 3))
        return snakeLinkSizes

    def Choose_Propagation_Stream(self, numLinks, direction):
        linkSizes = self.Choose_Link_Sizes()
        numJoints = numLinks - 1
        propAxis = np.random.randin(low=0, high=3, size=numLinks)

        relLinkPos = np.zeros((numLinks, 3))
        for link in range(1, numLinks):
            relLinkPos[link][propAxis[link-1]] = direction*linkSizes[link][propAxis[link-1]]/2
        
        relJointPos = np.zeros((numJoints, 3))
        relJointPos[0][propAxis[0]] = direction*linkSizes[0][propAxis[0]]/2
        for joint in range(1, numJoints):
            if propAxis[joint] == propAxis[joint-1]: ## no change in axis
                relJointPos[joint][propAxis[joint]] = direction*linkSizes[joint][propAxis[joint]]
            else: ## axis changed
                relJointPos[joint][propAxis[joint-1]] = linkSizes[joint][propAxis[joint-1]]/2
                relJointPos[joint][propAxis[joint]] = direction*linkSizes[joint][propAxis[joint]]/2

        return propAxis, relLinkPos, relJointPos, linkSizes

    def Construct_Main_Body(self, numLinks, faceIndex, direction):
        self.mainSizes = self.Choose_Link_Sizes(self.numLinks)
        numJoints = numLinks - 1

        relLinkPos = np.zeros((numLinks, 3))
        for link in range(1, numLinks):
            relLinkPos[link][faceIndex] = direction*self.mainSizes[link][faceIndex]/2
        
        relJointPos = np.zeros((numJoints, 3))
        relJointPos[0][faceIndex] = direction*self.mainSizes[0][faceIndex]/2
        for joint in range(1, numJoints):
            relJointPos[joint][faceIndex] = direction*self.mainSizes[joint][faceIndex]
        
        return faceIndex, relLinkPos, relJointPos, self.mainSizes
    
    def Construct_Limb(self, parent, numSubLinks, limbFace, limbDir):        
        linkSizes = self.Choose_Link_Sizes(numSubLinks)

        relLinkPos = np.zeros((numSubLinks, 3))
        relJointPos = np.zeros((numSubLinks, 3))

        if parent == 0:
            relJointPos[0] = self.origin
            relJointPos[0][limbFace] = self.origin[limbFace] + (limbDir * self.mainSizes[0][limbFace]/2)
        else:
            relJointPos[0][self.mainFace] = self.mainDir * self.mainSizes[parent][self.mainFace]/2
            relJointPos[0][limbFace] = limbDir * self.mainSizes[parent][limbFace]/2
        
        relLinkPos[0][limbFace] = limbDir * linkSizes[0][limbFace]/2
        
        for subLimb in range(1, numSubLinks):
            relJointPos[subLimb][limbFace] = limbDir * linkSizes[subLimb-1][limbFace]
            relLinkPos[subLimb][limbFace] = limbDir * linkSizes[subLimb][limbFace]/2

        return limbFace, relLinkPos, relJointPos, linkSizes

    def Get_Joints_and_Links(self):
        faceOpt = [0,1,2] # corresponding to x, y, or z, respectively
        dirOpt = [-1,1]

        self.mainFace = rd.choice(faceOpt)
        self.mainDir = rd.choice(dirOpt)
        mainBody = self.Construct_Main_Body(self.numLinks, self.mainFace, self.mainDir)

        self.links[0] = LINK(linkName = 0,
                            pos = self.origin, 
                            size = mainBody[3][0], 
                            sensorYN = rd.randint(0,1))
        self.joints[0] = JOINT(jointName = "0_1", 
                               parentLink = "0", 
                               childLink = "1",
                               jointType = "revolute",
                               jointPos = self.origin + mainBody[2][0],
                               jointAxis = self.Get_Joint_Axis(mainBody[0], rd.randint(0,1)))

        for linkIndex in range(1, self.numLinks):
            self.links[linkIndex] = LINK(linkName = linkIndex, 
                                        pos = mainBody[1][linkIndex],
                                        size = mainBody[3][linkIndex],
                                        sensorYN = rd.randint(0,1))
            if linkIndex < self.numLinks-1:
                parentLink = str(linkIndex)
                childLink = str(linkIndex+1)
                jointName = parentLink+"_"+childLink
                self.joints[linkIndex] = JOINT(jointName = jointName, 
                                                parentLink = parentLink, 
                                                childLink = childLink,
                                                jointType = "revolute",
                                                jointPos = mainBody[2][linkIndex],
                                                jointAxis = self.Get_Joint_Axis(mainBody[0], rd.randint(0, 1)))
        
        faceOpt.remove(self.mainFace)
        self.totalLinkTally = self.numLinks
        #limbYN = [0,0,0,0,1]
        limbYN = np.random.randint(low=0, high=3, size=self.numLinks)
        for parent in range(self.numLinks):
            if limbYN[parent] == 1: ## limb grown from only one direction on random axis
                #numSubLimbs = 2
                numSubLimbs = rd.randint(1, 5)
                limbStructure = self.Construct_Limb(parent, numSubLimbs, rd.choice(faceOpt), rd.choice(dirOpt))
                for subLimb in range(numSubLimbs):
                    childLink = str(self.totalLinkTally)
                    jointName = str(parent)+"_"+childLink
                    self.joints[self.totalLinkTally-1] = JOINT(jointName = jointName, 
                                                                parentLink = str(parent),
                                                                childLink = childLink,
                                                                jointType = "revolute",
                                                                jointPos = limbStructure[2][subLimb],
                                                                jointAxis = self.Get_Joint_Axis(limbStructure[0], rd.randint(0, 1)))
                    self.links[self.totalLinkTally] = LINK(linkName = self.totalLinkTally,
                                                        pos = limbStructure[1][subLimb],
                                                        size = limbStructure[3][subLimb],
                                                        sensorYN = rd.randint(0,1))
                    self.totalLinkTally += 1
            elif limbYN[parent] == 2: ## limb grown from both directions on random axis
                face = rd.choice(faceOpt)
                numSubLimbsPos = rd.randint(1, 5)
                numSubLimbsNeg = rd.randint(1, 5)
                limbStrPos = self.Construct_Limb(parent, numSubLimbsPos, face, 1)
                limbStrNeg = self.Construct_Limb(parent, numSubLimbsNeg, face, -1)
                for subLimb in range(numSubLimbsPos):
                    childLink = str(self.totalLinkTally)
                    jointName = str(parent)+"_"+childLink
                    self.joints[self.totalLinkTally-1] = JOINT(jointName = jointName, 
                                                                parentLink = str(parent),
                                                                childLink = childLink,
                                                                jointType = "revolute",
                                                                jointPos = limbStrPos[2][subLimb],
                                                                jointAxis = self.Get_Joint_Axis(limbStrPos[0], rd.randint(0, 1)))
                    self.links[self.totalLinkTally] = LINK(linkName = self.totalLinkTally,
                                                        pos = limbStrPos[1][subLimb],
                                                        size = limbStrPos[3][subLimb],
                                                        sensorYN = rd.randint(0,1))
                    self.totalLinkTally += 1
                for subLimb in range(numSubLimbsNeg):
                    childLink = str(self.totalLinkTally)
                    jointName = str(parent)+"_"+childLink
                    self.joints[self.totalLinkTally-1] = JOINT(jointName = jointName, 
                                                                parentLink = str(parent),
                                                                childLink = childLink,
                                                                jointType = "revolute",
                                                                jointPos = limbStrNeg[2][subLimb],
                                                                jointAxis = self.Get_Joint_Axis(limbStrNeg[0], rd.randint(0, 1)))
                    self.links[self.totalLinkTally] = LINK(linkName = self.totalLinkTally,
                                                        pos = limbStrNeg[1][subLimb],
                                                        size = limbStrNeg[3][subLimb],
                                                        sensorYN = rd.randint(0,1))
                    self.totalLinkTally += 1

        return self.links, self.joints, self.totalLinkTally
    
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