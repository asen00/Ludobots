import random as rd
import numpy as np

from snakeLink import LINK
from snakeJoint import JOINT

class HORSE_INFO:
    def __init__(self, numLinks):
        self.links = {}
        self.joints = {}
        self.origin = [0,0,5]

        # FIXING GEOMETRY OF MAIN SNAKE BODY
        self.numLinks = numLinks
        self.mainSizes = np.random.uniform(low=0.75, high=0.75, size=(self.numLinks, 3))
        self.mainFace = 0
        self.mainDir = 1
    
    def Choose_Limb_Link_Sizes(self, numLinks):
        LinkSizes = np.zeros((numLinks, 3))
        for sublimb in range(numLinks):
            LinkSizes[sublimb] = np.random.uniform(low=0.25-(0.05*sublimb), high=0.75-(0.1*sublimb), size=3)
        return LinkSizes

    def Construct_Main_Body(self, numLinks, faceIndex, direction):
        numJoints = numLinks - 1

        relLinkPos = np.zeros((numLinks, 3))
        for link in range(1, numLinks):
            relLinkPos[link][faceIndex] = direction*self.mainSizes[link][faceIndex]/2
        
        relJointPos = np.zeros((numJoints, 3))
        relJointPos[0][faceIndex] = direction*self.mainSizes[0][faceIndex]/2
        for joint in range(1, numJoints):
            relJointPos[joint][faceIndex] = direction*self.mainSizes[joint][faceIndex]
        
        return faceIndex, relLinkPos, relJointPos, self.mainSizes

    def Construct_Limb(self, parent, numSubLinks, limbFaces, zeroethDir):
        linkSizes = self.Choose_Limb_Link_Sizes(numSubLinks)
        
        limbDirs = np.zeros(numSubLinks, dtype=int)
        for sublimb in range(numSubLinks):
            if limbFaces[sublimb] == limbFaces[0]:
                limbDirs[sublimb] = zeroethDir
            else:
                limbDirs[sublimb] = rd.choice([-1,1])

        relLinkPos = np.zeros((numSubLinks, 3))
        relJointPos = np.zeros((numSubLinks, 3))

        if parent == 0:
            relJointPos[0] = self.origin
            relJointPos[0][limbFaces[0]] = self.origin[limbFaces[0]] + (limbDirs[0] * self.mainSizes[0][limbFaces[0]]/2)
            relLinkPos[0][limbFaces[0]] = limbDirs[0]*linkSizes[0][limbFaces[0]]/2
        
        else:
            relJointPos[0][self.mainFace] = self.mainDir * self.mainSizes[parent][self.mainFace]/2
            relJointPos[0][limbFaces[0]] = limbDirs[0] * self.mainSizes[parent][limbFaces[0]]/2

            relLinkPos[0][limbFaces[0]] = limbDirs[0] * linkSizes[0][limbFaces[0]]/2

        for subLimb in range(1, numSubLinks):
            if limbFaces[subLimb] == limbFaces[subLimb-1]:
                relJointPos[subLimb][limbFaces[subLimb]] = limbDirs[subLimb] * linkSizes[subLimb-1][limbFaces[subLimb]]
            else:
                relJointPos[subLimb][limbFaces[subLimb-1]] = limbDirs[subLimb-1] * linkSizes[subLimb-1][limbFaces[subLimb-1]]/2
                relJointPos[subLimb][limbFaces[subLimb]] = limbDirs[subLimb] * linkSizes[subLimb-1][limbFaces[subLimb]]/2
            relLinkPos[subLimb][limbFaces[subLimb]] = limbDirs[subLimb] * linkSizes[subLimb][limbFaces[subLimb]]/2

        return relLinkPos, relJointPos, linkSizes

    def Get_Joints_and_Links(self):
        faceOpt = [0,1,2] # corresponding to x, y, or z, respectively
        dirOpt = [-1,1]

        if self.numLinks > 1:
            limbYN = np.random.randint(low=0, high=3, size=self.numLinks)
            mainBody = self.Construct_Main_Body(self.numLinks, self.mainFace, self.mainDir)

            self.links[0] = LINK(linkName = 0,
                                pos = self.origin, 
                                size = mainBody[3][0], 
                                sensorYN = 1)
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
                                            sensorYN = 1)
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
        else:
            limbYN = np.random.randint(low=1, high=3, size=self.numLinks)
            self.links[0] = LINK(linkName = 0,
                                pos = self.origin, 
                                size = np.random.uniform(low=0.75, high=0.75, size=3), 
                                sensorYN = 1)
        
        faceOpt.remove(self.mainFace)
        self.totalLinkTally = self.numLinks
        for parent in range(self.numLinks):
            if limbYN[parent] == 1: ## limb grown from only one direction on random axis
                numSubLimbs = rd.randint(1, 3)
                limbFaces = np.random.choice(faceOpt, size=numSubLimbs)
                limbStructure = self.Construct_Limb(parent, numSubLimbs, limbFaces, rd.choice(dirOpt))
                for subLimb in range(numSubLimbs):
                    if subLimb == 0:
                        childLink = str(self.totalLinkTally)
                        jointName = str(parent)+"_"+childLink
                        self.joints[self.totalLinkTally-1] = JOINT(jointName = jointName, 
                                                                    parentLink = str(parent),
                                                                    childLink = childLink,
                                                                    jointType = "revolute",
                                                                    jointPos = limbStructure[1][subLimb],
                                                                    jointAxis = self.Get_Joint_Axis(limbFaces[subLimb], rd.randint(0, 1)))
                        self.links[self.totalLinkTally] = LINK(linkName = self.totalLinkTally,
                                                            pos = limbStructure[0][subLimb],
                                                            size = limbStructure[2][subLimb],
                                                            sensorYN = rd.randint(0,1))
                    else:
                        parentLink = str(self.totalLinkTally-1)
                        childLink = str(self.totalLinkTally)
                        jointName = parentLink+"_"+childLink
                        self.joints[self.totalLinkTally-1] = JOINT(jointName = jointName, 
                                                                    parentLink = parentLink,
                                                                    childLink = childLink,
                                                                    jointType = "revolute",
                                                                    jointPos = limbStructure[1][subLimb],
                                                                    jointAxis = self.Get_Joint_Axis(limbFaces[subLimb], rd.randint(0, 1)))
                        self.links[self.totalLinkTally] = LINK(linkName = self.totalLinkTally,
                                                            pos = limbStructure[0][subLimb],
                                                            size = limbStructure[2][subLimb],
                                                            sensorYN = rd.randint(0,1))
                    self.totalLinkTally += 1
            elif limbYN[parent] == 2: ## limb grown from both directions on random axis
                numSubLimbsPos = rd.randint(1, 3)
                numSubLimbsNeg = rd.randint(1, 3)
                limbFacesPos = np.random.choice(faceOpt, size=numSubLimbs)
                limbFacesNeg = np.random.choice(faceOpt, size=numSubLimbs)
                limbStrPos = self.Construct_Limb(parent, numSubLimbsPos, limbFacesPos, 1)
                limbStrNeg = self.Construct_Limb(parent, numSubLimbsNeg, limbFacesNeg, -1)
                for subLimb in range(numSubLimbsPos):
                    if subLimb == 0:
                        childLink = str(self.totalLinkTally)
                        jointName = str(parent)+"_"+childLink
                        self.joints[self.totalLinkTally-1] = JOINT(jointName = jointName, 
                                                                    parentLink = str(parent),
                                                                    childLink = childLink,
                                                                    jointType = "revolute",
                                                                    jointPos = limbStrPos[1][subLimb],
                                                                    jointAxis = self.Get_Joint_Axis(limbStrPos[subLimb], rd.randint(0, 1)))
                        self.links[self.totalLinkTally] = LINK(linkName = self.totalLinkTally,
                                                            pos = limbStrPos[0][subLimb],
                                                            size = limbStrPos[2][subLimb],
                                                            sensorYN = rd.randint(0,1))
                    else:
                        parentLink = str(self.totalLinkTally-1)
                        childLink = str(self.totalLinkTally)
                        jointName = parentLink+"_"+childLink
                        self.joints[self.totalLinkTally-1] = JOINT(jointName = jointName, 
                                                                    parentLink = parentLink,
                                                                    childLink = childLink,
                                                                    jointType = "revolute",
                                                                    jointPos = limbStrPos[1][subLimb],
                                                                    jointAxis = self.Get_Joint_Axis(limbStrPos[subLimb], rd.randint(0, 1)))
                        self.links[self.totalLinkTally] = LINK(linkName = self.totalLinkTally,
                                                            pos = limbStrPos[0][subLimb],
                                                            size = limbStrPos[2][subLimb],
                                                            sensorYN = rd.randint(0,1))
                    self.totalLinkTally += 1
                for subLimb in range(numSubLimbsNeg):
                    if subLimb == 0:
                        childLink = str(self.totalLinkTally)
                        jointName = str(parent)+"_"+childLink
                        self.joints[self.totalLinkTally-1] = JOINT(jointName = jointName, 
                                                                    parentLink = str(parent),
                                                                    childLink = childLink,
                                                                    jointType = "revolute",
                                                                    jointPos = limbStrNeg[1][subLimb],
                                                                    jointAxis = self.Get_Joint_Axis(limbStrNeg[subLimb], rd.randint(0, 1)))
                        self.links[self.totalLinkTally] = LINK(linkName = self.totalLinkTally,
                                                            pos = limbStrNeg[0][subLimb],
                                                            size = limbStrNeg[2][subLimb],
                                                            sensorYN = rd.randint(0,1))
                    else:
                        parentLink = str(self.totalLinkTally-1)
                        childLink = str(self.totalLinkTally)
                        jointName = parentLink+"_"+childLink
                        self.joints[self.totalLinkTally-1] = JOINT(jointName = jointName, 
                                                                    parentLink = parentLink,
                                                                    childLink = childLink,
                                                                    jointType = "revolute",
                                                                    jointPos = limbStrNeg[1][subLimb],
                                                                    jointAxis = self.Get_Joint_Axis(limbStrNeg[subLimb], rd.randint(0, 1)))
                        self.links[self.totalLinkTally] = LINK(linkName = self.totalLinkTally,
                                                            pos = limbStrNeg[0][subLimb],
                                                            size = limbStrNeg[2][subLimb],
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