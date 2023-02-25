import pybullet as p
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import numpy as np

from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:
    def __init__(self, solutionID, world):
        self.sensors = {}
        self.motors = {}

        self.world = world
        
        self.myID = str(solutionID)
        
        self.robotId = p.loadURDF("horse"+self.myID+".urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.nn = NEURAL_NETWORK("horse"+self.myID+".nndf")
        
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        os.system(f"rm brain{solutionID}.nndf")
    
    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, timeStep):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(timeStep)
    
    def Think(self):
        self.nn.Update()
        #self.nn.Print()
    
    def Act(self, robotId, timeStep):
        for neuron in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuron):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuron)
                desiredAngle = c.motorJointRange * self.nn.Get_Value_Of(neuron)
                self.motors[jointName].Set_Value(robotId, desiredAngle)
    
    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        f = open("tmp"+self.myID+".txt", "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()
        os.system("mv tmp"+self.myID+".txt HORSEfitness"+self.myID+".txt")