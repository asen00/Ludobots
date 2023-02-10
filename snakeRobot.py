import pybullet as p
import pyrosim.pyrosim as pyrosim
import os
import constants as c
import numpy as np

from snake import SNAKE
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:
    def __init__(self, world, origin):
        self.sensors = {}
        self.motors = {}

        self.world = world

        self.snake = SNAKE(origin)
        self.snake.Generate_Simulation()
        self.robotId = p.loadURDF("snake.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)

        self.nn = NEURAL_NETWORK("snake.nndf")
        
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
    
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
        positionOfBox = p.getBasePositionAndOrientation(self.world.bodyID)[0]

        stateOfTracker = p.getLinkState(self.robotId,4)
        positionOfTracker = stateOfTracker[0]
        print(positionOfBox)
        xdistT = np.abs(positionOfBox[0]+1.5 - positionOfTracker[0])
        ydistT = np.abs(positionOfBox[1]-1 - positionOfTracker[1])

        optimize = xdistT*ydistT

        f = open("tmp"+self.myID+".txt", "w")
        f.write(str(optimize))
        os.system("mv tmp"+self.myID+".txt fitness"+self.myID+".txt")
        f.close()