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
        
        self.robotId = p.loadURDF("miscStorage/horse"+self.myID+".urdf", flags=p.URDF_USE_SELF_COLLISION|p.URDF_USE_SELF_COLLISION_INCLUDE_PARENT)
        ## If you turn off self-collisions, then you need to make the limbs propagate in a single direction. Ask Sam what he means by space-filling.
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.nn = NEURAL_NETWORK("miscStorage/horse"+self.myID+".nndf")
        
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        os.system(f"rm miscStorage/horse{solutionID}.nndf")
        os.system(f"rm miscStorage/horse{solutionID}.urdf")
    
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
        f = open("miscStorage/tmp"+self.myID+".txt", "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()
        os.system("mv miscStorage/tmp"+self.myID+".txt miscStorage/HORSEfitness"+self.myID+".txt")