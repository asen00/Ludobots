import random as rd
import numpy as np

from snakeLink import LINK
from snakeJoint import JOINT

class SNAKE_INFO: 
    def __init__(self, numLinks, origin):
        self.numLinks = numLinks
        self.origin = origin
        self.links = {}
        self.joints = {}
        self.linkXsize = np.random.random(size=self.numLinks)*rd.random()+rd.random()

    '''def Get_Links(self):
        ## Absolute position
        self.linkXpos[0] = self.origin[0]
        self.linkXsize[0] = 0.7
        self.links[0] = LINK(0, self.origin, [self.linkXsize[0], 0.6, 0.5], rd.randint(0,1))

        ## Relative to upstream joint
        for linkName in range(1, self.numLinks):
            self.linkXsize[linkName] = 0.7
            self.linkXpos[linkName] = self.linkXsize[linkName]/2
            #self.linkXpos[linkName] = self.links[linkName-1].pos[0] + self.links[linkName-1].size[0]/2
            
            self.links[linkName] = LINK(linkName, [self.linkXpos[linkName], self.origin[1], self.origin[2]], [self.linkXsize[linkName], 0.6, 0.5], rd.randint(0,1))
        
        return self.links   

    def Get_Joints(self):
        ## Absolute position
        self.joints[0] = JOINT("0_1", "0", "1", self.links[0].Get_Front_Joint_Pos(), self.Get_Joint_Axis(rd.randint(0,1)))

        ## Relative to previous joint
        for i in range(1, self.numLinks-1):
            parentLink = str(i)
            childLink = str(i+1)
            jointName = parentLink+"_"+childLink
            #jointPos = [self.joints[i-1].jointPos[0] + self.links[i].size[0], self.joints[i-1].jointPos[1], self.joints[i-1].jointPos[2]]
            jointPos = [self.links[i].size[0], self.joints[0].jointPos[1], self.joints[0].jointPos[2]]

            self.joints[i] = JOINT(jointName, parentLink, childLink, jointPos, self.Get_Joint_Axis(rd.randint(1,3)))
        
        return self.joints'''
    
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