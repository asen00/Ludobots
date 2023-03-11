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
        
        self.sensors = {}
        self.sensorCount = 0
        for link in self.info[0]:
            if self.info[0][link].sensorYN==1:
                self.sensors[link] = self.sensorCount
                self.sensorCount += 1

        self.joints = {}
        self.jointCount = 0
        for joint in self.info[1]:
            self.joints[joint] = self.jointCount
            self.jointCount += 1

        self.remainingLinks = list(self.info[0].keys())
        self.remainingJoints = list(self.info[1].keys())

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
        randomChange = rd.randint(0, 2)
        #randomChange = 3
        if randomChange == 0:
            randomSublink = rd.choice(self.remainingLinks[4:])
            self.Change_Link_Size(randomSublink)
        elif randomChange == 1:
            randomSublink = rd.choice(self.remainingLinks)
            self.Change_Sensing(randomSublink)
        elif randomChange == 2:
            randomSublink = rd.choice(self.remainingLinks)
            self.Add_Sublink(randomSublink)
        else:
            randomSublink = rd.choice(self.remainingLinks[3:])
            self.Remove_Sublink(randomSublink)
        
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
            self.info[0][link].sensorYN = 1
            self.info[3] += 1
            
            higherlinkindex = []
            for i in list(self.sensors.keys()):
                if i > link:
                    higherlinkindex.append(i)
                    self.sensors[i] += 1
            
            if len(higherlinkindex) > 0:
                linkReq = np.min(higherlinkindex)            
                self.weights = np.insert(self.weights, obj=self.sensors[linkReq], values=(2*np.random.rand(self.info[4]))-1, axis=0)
                self.sensors.update({link: self.sensors[linkReq]-1})
            else:
                self.weights = np.append(self.weights, values=[(2*np.random.rand(self.info[4]))-1], axis=0)
                self.sensors.update({link: self.sensorCount})
            
            self.sensorCount += 1
        
        else:
            self.info[0][link].sensorYN = 0
            self.info[3] -= 1
            self.weights = np.delete(self.weights, obj=self.sensors[link], axis=0)
            del self.sensors[link]
            self.sensorCount -= 1
            for i in list(self.sensors.keys()):
                if i > link:
                    self.sensors[i] -= 1

    def Remove_Sublink(self, link):
        print('start', self.info[1])   
        if self.info[0][link].pieceType == 'start':
            pass
        elif self.info[0][link].pieceType == 'end':
            if self.info[0][link].sensorYN == 1:
                self.info[3] -= 1
                self.weights = np.delete(self.weights, obj=self.sensors[link], axis=0)
                del self.sensors[link]
                self.sensorCount -= 1
            self.info[2] -= 1
            self.info[4] -= 1
            del self.info[0][link]
            del self.info[1][link-1]
            self.weights = np.delete(self.weights, obj=link-1, axis=1)
            self.remainingLinks.remove(link)
            self.remainingJoints.remove(link-1)
        else:
            print('middle')
            self.info[0][link] = self.info[0][link+1] # turn link 9 into link 10

            if self.info[0][link+1].pieceType == 'end': # if 10 is the end piece
                if self.info[0][link+1].sensorYN == 1: # if 10 has a sensor
                    self.info[3] -= 1 # decrease numsensors by one
                    self.weights = np.delete(self.weights, obj=self.sensors[link+1], axis=0) # delete the row for the sensor in link 10
                    del self.sensors[link+1] # delete the sensor in link 10
                    self.sensorCount -= 1 # decrease numsensors by one
                self.info[2] -= 1 # decrease numtotallinks by one
                self.info[4] -= 1 # decrease nummotors by one
                del self.info[0][link+1] # delete link 10
                del self.info[1][link] # delete joint 9, i.e., joint between links 9 and 10
                self.weights = np.delete(self.weights, obj=link, axis=1) # delete the column for the motor in joint 9
                self.remainingLinks.remove(link+1) # delete link 10
                self.remainingJoints.remove(link) # delete joint 9, i.e., joint between links 9 and 10
                # then you need to rename the joints after joint 9 to be indexed by one number smaller
                for index in range(len(self.remainingJoints)):
                    if self.remainingJoints[index] >= link+1:
                        self.remainingJoints[index] -= 1
                '''STUCK: Need to rename key in self.info[1] dict, such that all joints after the deleted one are indexed by a smaller index'''
            else:
                print('ERROR in Remove_Sublink() method from horse.py')
        print('end', self.info[1])

    def Add_Sublink(self, link):
        if link-4 in range(3):
            print('pass')
            pass
        elif self.info[0][link].pieceType != 'end':
            print('pass')
            pass
        else:
            print('link after which new link is being created: ', link)
            print('new link key: ', self.info[2])
            newlinksize = np.random.uniform(low=0.25, high=0.5, size=3)
            jointPos = np.zeros(3)
            jointPos[np.abs(self.info[0][link].sublimbFace)] = np.sign(self.info[0][link].sublimbFace) * self.info[0][link].size[np.abs(self.info[0][link].sublimbFace)]
            linkpos = np.zeros(3)
            linkpos[np.abs(self.info[0][link].sublimbFace)] = np.sign(self.info[0][link].sublimbFace) * newlinksize[np.abs(self.info[0][link].sublimbFace)]/2
            sensorYN = 0
            
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
            self.info[2] += 1
            self.info[4] += 1
            newMotorWeights = np.swapaxes([(2*np.random.rand(self.info[3]))-1], 0, 1)
            self.weights = np.append(self.weights, newMotorWeights, axis=1)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[5,-3,0], size=[1,1,1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("miscStorage/horse"+str(self.myID)+".urdf")

        for link in self.remainingLinks:
            pyrosim.Send_Cube(name = str(link), pos = self.info[0][link].pos, size = self.info[0][link].size, sensorYN=self.info[0][link].sensorYN)
        
        for joint in self.remainingJoints:
            pyrosim.Send_Joint(name = self.info[1][joint].jointName,
                                    parent= self.info[1][joint].parentLink, 
                                    child = self.info[1][joint].childLink, 
                                    type = self.info[1][joint].jointType, 
                                    position = self.info[1][joint].jointPos, 
                                    jointAxis = self.info[1][joint].jointAxis)

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("miscStorage/horse"+str(self.myID)+".nndf")
        
        sensorCount = 0
        for i in list(self.sensors.keys()):
            if self.info[0][i].sensorYN == 1: ## link has a sensor
                pyrosim.Send_Sensor_Neuron(name = sensorCount, linkName = self.info[0][i].linkName)
                sensorCount += 1
        
        motorCount = 0
        for i in self.remainingJoints:
            pyrosim.Send_Motor_Neuron(name = sensorCount+i , jointName = self.info[1][i].jointName)
            motorCount += 1

        print(self.weights.shape)
        for i in list(self.sensors.keys()):
            currentRow = self.sensors[i]
            for j in self.remainingJoints:
                currentColumn = j
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn, weight = self.weights[currentRow][currentColumn])
        
        pyrosim.End()