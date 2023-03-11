import pyrosim.pyrosim as pyrosim
import random as rd
import numpy as np
import time
import os

from horseInfo import HORSE_INFO
from snakeLink import LINK
from snakeJoint import JOINT

class HORSE_SOLUTION:
    def __init__(self, solutionID):
        self.myID = str(solutionID)

        self.numLinks = 3
        self.horse = HORSE_INFO(self.numLinks)
        self.info = self.horse.Get_Joints_and_Links()
        self.weights = (2*np.random.rand(self.info[3],self.info[4]))-1
        print(self.weights.shape)
        
        self.sensors = {}
        self.sensorCount = 0
        for link in self.info[0]:
            if self.info[0][link].sensorYN==1:
                self.sensors[link] = self.sensorCount
                self.sensorCount += 1

        '''
        For reference:
        self.links = self.info[0]
        self.joints = self.info[1]
        self.totalLinks = self.info[2]
        self.numSensors = self.info[3]
        self.numMotors = self.info[4]
        '''

        #self.minZpos = self.info.minZpos
    
    def Set_ID(self, childID):
        self.myID = str(childID)

    def Start_Simulation(self, directOrGUI):
        self.Generate_Body()
        self.Generate_Brain()
        os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python horseSimulate.py " + " " + directOrGUI + " " + self.myID + " 2>&1 &")
    
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("miscStorage/HORSEfitness"+self.myID+".txt"):
            time.sleep(0.01)
        
        success = False
        while not success:
            try:
                fitnessFile = open("miscStorage/HORSEfitness"+self.myID+".txt", "r")
                self.fitness = float(fitnessFile.read())
                #print(self.fitness)
                fitnessFile.close()
                success = True
            except:
                time.sleep(0.01)
        
        os.system("rm miscStorage/HORSEfitness"+self.myID+".txt")

    def Mutate(self):
        randomChange = rd.randint(0, 3)
        remainingLinkIndices = list(self.info[0].keys())
        print(randomChange)
        print(remainingLinkIndices)
        if randomChange == 0:
            randomSublink = rd.choice(remainingLinkIndices[4:])
            self.Change_Link_Size(randomSublink)
        elif randomChange == 1:
            randomSublink = rd.choice(remainingLinkIndices)
            self.Change_Sensing(randomSublink)
        elif randomChange == 2:
            randomSublink = rd.choice(remainingLinkIndices[3:])
            self.Remove_Sublink(randomSublink)
        else:
            randomSublink = rd.choice(remainingLinkIndices)
            self.Add_Sublink(randomSublink)
        
        ## Changing random synaptic weight
        randomRow = rd.randint(0, self.info[3]-1)
        randomColumn = rd.randint(0, self.info[4]-1)
        self.weights[randomRow, randomColumn] = rd.random() * 2 - 1

    def Change_Link_Size(self, link):
        subsequentJointIndex = link
        if self.info[0][link].pieceType == 'start':
            pass
        else:
            self.info[0][link].size = np.random.uniform(0.1, 0.5, size=3)
            self.info[0][link].pos[np.abs(self.info[0][link].sublimbFace)] = np.sign(self.info[0][link].sublimbFace)*self.info[0][link].size[np.abs(self.info[0][link].sublimbFace)]/2
            if self.info[0][link].pieceType == 'middle':
                if np.abs(self.info[0][link].sublimbFace) == np.abs(self.info[0][link+1].sublimbFace):
                    self.info[1][subsequentJointIndex].jointPos[np.abs(self.info[0][link].sublimbFace)] = np.sign(self.info[0][link].sublimbFace)*self.info[0][link].size[np.abs(self.info[0][link].sublimbFace)]
                else:
                    self.info[1][subsequentJointIndex].jointPos[np.abs(self.info[0][link].sublimbFace)] = np.sign(self.info[0][link].sublimbFace)*self.info[0][link].size[np.abs(self.info[0][link].sublimbFace)]/2
                    self.info[1][subsequentJointIndex].jointPos[np.abs(self.info[0][link+1].sublimbFace)] = np.sign(self.info[0][link+1].sublimbFace)*self.info[0][link].size[np.abs(self.info[0][link+1].sublimbFace)]/2

    def Change_Sensing(self, link):
        if self.info[0][link].sensorYN == 0:
            self.info[0][link].sensorYN == 1
            self.info[3] += 1
            self.sensors[link] = self.sensorCount
            self.sensorCount += 1
            np.insert(self.weights, obj=self.sensors[link+1], values=(2*np.random.rand(self.info[4]))-1, axis=0)
            print(self.weights.shape)
        else:
            self.info[0][link].sensorYN == 0
            self.info[3] -= 1
            np.delete(self.weights, obj=self.sensors[link], axis=0)
            print(self.weights.shape)
            del self.sensors[link]
            self.sensorCount -= 1

    def Remove_Sublink(self, link):
        if self.info[0][link].pieceType == 'start':
            print('start')
            pass
        elif self.info[0][link].pieceType == 'end':
            print('end')
            if self.info[0][link].sensorYN == 1:
                self.info[3] -= 1
                np.delete(self.weights, obj=self.sensors[link], axis=0)
                print(self.weights.shape)
                del self.sensors[link]
                self.sensorCount -= 1
            self.info[2] -= 1
            self.info[4] -= 1
            del self.info[0][link]
            del self.info[1][link-1]
            np.delete(self.weights, obj=link-1, axis=1)
            print(self.weights.shape)
        else:
            print('middle')
            self.info[0][link] = self.info[0][link+1]
            if self.info[0][link].sensorYN == 1:
                self.info[3] -= 1
                np.delete(self.weights, obj=self.sensors[link], axis=0)
                print(self.weights.shape)
                del self.sensors[link]
                self.sensorCount -= 1
            self.info[2] -= 1
            self.info[4] -= 1
            del self.info[0][link+1]
            np.delete(self.weights, obj=link-1, axis=1)
            print(self.weights.shape)

    def Add_Sublink(self, link):
        if self.info[1][link-4].jointName[0] in range(3):
            pass
        elif self.info[0][link].pieceType != 'end':
            pass
        else:
            newlinksize = np.random.uniform(low=0.25, high=0.5, size=3)
            jointPos = np.zeros(3)
            jointPos[np.abs(self.info[0][link].sublimbFace)] = np.sign(self.info[0][link].sublimbFace) * self.info[0][link].size[np.abs(self.info[0][link].sublimbFace)]
            linkpos = np.zeros(3)
            linkpos[np.abs(self.info[0][link].sublimbFace)] = np.sign(self.info[0][link].sublimbFace) * newlinksize[np.abs(self.info[0][link].sublimbFace)]/2
            sensorYN = rd.randint(0,1)
            
            self.info[1][self.info[2]-1] = JOINT(jointName = str(link)+'_'+str(self.info[2]), 
                                                    parentLink = str(link),
                                                    childLink = str(self.info[2]),
                                                    jointType = "revolute",
                                                    jointPos = jointPos,
                                                    jointAxis = self.info[1][link-1].jointAxis)
            self.info[0][self.info[2]] = LINK(linkName = self.info[2], 
                                            pos = linkpos,
                                            size = newlinksize,
                                            sensorYN = sensorYN,
                                            pieceType = 'end',
                                            sublimbFace = self.info[0][link].sublimbFace)
            
            if sensorYN == 1:
                self.info[3] += 1
                np.append(self.weights, [(2*np.random.rand(self.info[4]))-1], axis=0)
                print(self.weights.shape)
                self.sensors[self.info[2]] = self.sensorCount
                self.sensorCount += 1
            self.info[2] += 1
            self.info[4] += 1
            np.append(self.weights, np.swapaxes([(2*np.random.rand(self.info[3]))-1], 0, 1), axis=1)
            print(self.weights.shape)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[5,-3,0], size=[1,1,1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("miscStorage/horse"+str(self.myID)+".urdf")
        
        for i in range(self.info[2]):
            pyrosim.Send_Cube(name = str(i), pos = self.info[0][i].pos, size = self.info[0][i].size, sensorYN=self.info[0][i].sensorYN)
            if i < self.info[2]-1:
                pyrosim.Send_Joint(name = self.info[1][i].jointName,
                                    parent= self.info[1][i].parentLink, 
                                    child = self.info[1][i].childLink, 
                                    type = self.info[1][i].jointType, 
                                    position = self.info[1][i].jointPos, 
                                    jointAxis = self.info[1][i].jointAxis)

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("miscStorage/horse"+str(self.myID)+".nndf")
        
        sensorCount = 0
        for i in range(self.info[2]):
            if self.info[0][i].sensorYN == 1: ## link has a sensor
                pyrosim.Send_Sensor_Neuron(name = sensorCount, linkName = self.info[0][i].linkName)
                sensorCount += 1
        
        motorCount = 0
        for i in range(self.info[2]-1):
            pyrosim.Send_Motor_Neuron(name = sensorCount+i , jointName = self.info[1][i].jointName)
            motorCount += 1

        #print(self.weights.shape, self.info[3], self.info[4])
        for currentRow in range(self.info[3]):
            for currentColumn in range(self.info[4]):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn, weight = self.weights[currentRow][currentColumn])
        
        pyrosim.End()