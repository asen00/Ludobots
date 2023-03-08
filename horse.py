import pyrosim.pyrosim as pyrosim
import random as rd
import numpy as np
import time
import os

from horseInfo import HORSE_INFO

class HORSE_SOLUTION:
    def __init__(self, solutionID):
        self.myID = str(solutionID)

        self.numLinks = rd.randint(1,5)
        self.info = HORSE_INFO(self.numLinks)
        self.linksAndjoints = self.info.Get_Joints_and_Links()
        self.links = self.linksAndjoints[0]
        self.joints = self.linksAndjoints[1]
        self.totalLinks = self.linksAndjoints[2]

        self.minZpos = self.info.minZpos

        self.numSensorNeurons = 0
        for i in range(self.totalLinks):
            if self.links[i].sensorYN == 1: ## link has a sensor
                self.numSensorNeurons += 1
        self.numMotorNeurons = 0
        for i in range(self.totalLinks-1):
            self.numMotorNeurons += 1
        self.weights = (2*np.random.rand(self.numSensorNeurons,self.numMotorNeurons))-1
    
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
        randomRow = rd.randint(0, self.numSensorNeurons-1)
        randomColumn = rd.randint(0, self.numMotorNeurons-1)
        self.weights[randomRow, randomColumn] = rd.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[5,-3,0] , size=[1,1,1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("miscStorage/horse"+str(self.myID)+".urdf")
        
        for i in range(self.totalLinks):
            pyrosim.Send_Cube(name = str(i), pos = self.links[i].pos, size = self.links[i].size, sensorYN=self.links[i].sensorYN)
            if i < self.totalLinks-1:
                pyrosim.Send_Joint(name = self.joints[i].jointName,
                                    parent= self.joints[i].parentLink, 
                                    child = self.joints[i].childLink, 
                                    type = self.joints[i].jointType, 
                                    position = self.joints[i].jointPos, 
                                    jointAxis = self.joints[i].jointAxis)

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("miscStorage/horse"+str(self.myID)+".nndf")
        
        sensorCount = 0
        for i in range(self.totalLinks):
            if self.links[i].sensorYN == 1: ## link has a sensor
                pyrosim.Send_Sensor_Neuron(name = sensorCount, linkName = self.links[i].linkName)
                sensorCount += 1
        
        motorCount = 0
        for i in range(self.totalLinks-1):
            pyrosim.Send_Motor_Neuron(name = sensorCount+i , jointName = self.joints[i].jointName)
            motorCount += 1

        for currentRow in range(self.numSensorNeurons):
            for currentColumn in range(self.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn, weight = self.weights[currentRow][currentColumn])
        
        pyrosim.End()