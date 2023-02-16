import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random as rd

from horseInfo import HORSE_INFO

class HORSE:
    def __init__(self, origin):
        # self.numLinks = 5
        self.numLinks = rd.randint(6,15)
        self.info = HORSE_INFO(self.numLinks, origin)
        self.links = self.info.Get_Joints_and_Links()[0]
        self.joints = self.info.Get_Joints_and_Links()[1]

    def Generate_Simulation(self):
        self.Generate_Snake_Body()
        self.Generate_Snake_Brain()

    def Generate_Snake_Body(self):
        pyrosim.Start_URDF("horse.urdf")
        
        for i in range(self.numLinks):
            pyrosim.Send_Cube(name = str(i), pos = self.links[i].pos, size = self.links[i].size, sensorYN=self.links[i].sensorYN)
            if i < self.numLinks-1:
                pyrosim.Send_Joint(name = self.joints[i].jointName,
                                    parent= self.joints[i].parentLink, 
                                    child = self.joints[i].childLink, 
                                    type = self.joints[i].jointType, 
                                    position = self.joints[i].jointPos, 
                                    jointAxis = self.joints[i].jointAxis)
        
        pyrosim.End()
    
    def Generate_Snake_Brain(self):
        pyrosim.Start_NeuralNetwork("horse.nndf")
        
        numSensorNeurons = 0
        for i in range(self.numLinks):
            if self.links[i].sensorYN == 1: ## link has a sensor
                pyrosim.Send_Sensor_Neuron(name = numSensorNeurons, linkName = self.links[i].linkName)
                numSensorNeurons += 1
        
        numMotorNeurons = 0
        for i in range(self.numLinks-1):
            pyrosim.Send_Motor_Neuron(name = numSensorNeurons+i , jointName = self.joints[i].jointName)
            numMotorNeurons += 1

        for currentRow in range(numSensorNeurons):
            for currentColumn in range(numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn, weight = rd.random())
        
        pyrosim.End()