import pybullet as p
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import math

from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:
    def __init__(self, solutionID):
        self.sensors = {}
        self.motors = {}

        self.robotId = p.loadURDF("body.urdf", flags = p.URDF_USE_SELF_COLLISION | p.URDF_USE_SELF_COLLISION_INCLUDE_PARENT)
        pyrosim.Prepare_To_Simulate(self.robotId)
        
        self.myID = str(solutionID)

        self.nn = NEURAL_NETWORK("brain"+self.myID+".nndf")
        
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
                desiredVelocity = self.nn.Get_Value_Of(neuron)
                self.motors[jointName].Set_Value(robotId, desiredVelocity)
    
    def Get_Fitness(self):
        stateOfTracker = p.getLinkState(self.robotId,3)
        centerofmassOfTracker = stateOfTracker[0]
        xdist = centerofmassOfTracker[0]+0.125-(-3.5)
        ydist = centerofmassOfTracker[1]+0.125-(2)
        zdist = centerofmassOfTracker[2]+0.25-(0.75)
        distanceFromBox = math.sqrt((xdist**2)+(ydist**2)+(zdist**2))
        f = open("tmp"+self.myID+".txt", "w")
        f.write(str(distanceFromBox))
        os.system("mv tmp"+self.myID+".txt fitness"+self.myID+".txt")
        f.close()