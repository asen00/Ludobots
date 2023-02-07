import pyrosim.pyrosim as pyrosim
import numpy as np
import random as rd
import constants as c
import time
import os

class SOLUTION:
    def __init__(self, ID):        
        self.weights = (2*np.random.rand(c.numSensorNeurons,c.numMotorNeurons))-1

        self.myID = str(ID)

    def Set_ID(self, childID):
        self.myID = str(childID)

    def Start_Simulation(self, directOrGUI):
        self.Generate_Brain()
        self.Generate_Body()
        os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python test1.py " + directOrGUI + " " + self.myID + " 2>&1 &")
    
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness"+self.myID+".txt"):
            time.sleep(0.01)
        
        success = False
        while not success:
            try:
                fitnessFile = open("fitness"+self.myID+".txt", "r")
                self.fitness = float(fitnessFile.read())
                #print(self.fitness)
                fitnessFile.close()
                success = True
            except:
                time.sleep(0.01)
        
        os.system("rm fitness"+self.myID+".txt")

    def Mutate(self):
        randomRow = rd.randint(0,c.numSensorNeurons-1)
        randomColumn = rd.randint(0,c.numMotorNeurons-1)
        self.weights[randomRow, randomColumn] = rd.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0,3,0.5] , size=[1,1,1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        
        # Link 1
        pyrosim.Send_Cube(name="Link1", pos=[0,0,1.25] , size=[3,2,0.5])

        # Wheel 1 joint
        pyrosim.Send_Joint(name = "Link1_Wheel1" , parent= "Link1" , child = "Wheel1" , type = "continuous", position = [-0.75,0,1], jointAxis = "0 1 0")
        
        # Wheel 1
        pyrosim.Send_Sphere(name="Wheel1", pos=[0,0,-0.5] , size=[0.5])
        
        # Link1_Link2 joint
        pyrosim.Send_Joint(name = "Link1_Link2" , parent= "Link1" , child = "Link2" , type = "fixed", position = [1.5,0,1.25], jointAxis = "0 1 0")
        
        # Link 2
        pyrosim.Send_Cube(name="Link2", pos=[0.125,-0.125,0], size=[0.25,1.75,0.5])

        # Link2_Tracker joint
        pyrosim.Send_Joint(name = "Link2_Tracker" , parent= "Link2" , child = "Tracker" , type = "fixed", position = [0.125,0.75,0], jointAxis = "0 1 0")

        # Tracker
        pyrosim.Send_Cube(name="Tracker", pos=[0,0.125,0], size=[0.25,0.25,0.5])
        
        # Link2_Link3 joint
        pyrosim.Send_Joint(name = "Link2_Link3" , parent= "Link2" , child = "Link3" , type = "fixed", position = [0.25,0,0], jointAxis = "0 1 0")

        # Link 3
        pyrosim.Send_Cube(name="Link3", pos=[0.5,1,0] , size=[1,4,0.5])
        
        # Wheel 2 joint
        pyrosim.Send_Joint(name = "Link3_Wheel2" , parent= "Link3" , child = "Wheel2" , type = "fixed", position = [0.5,2.5,-0.25], jointAxis = "0 1 0")
        
        # Wheel 2
        pyrosim.Send_Sphere(name="Wheel2", pos=[0,0,-0.5] , size=[0.5])

        # Wheel 3 joint
        pyrosim.Send_Joint(name = "Link3_Wheel3" , parent= "Link3" , child = "Wheel3" , type = "continuous", position = [0.5,0,-0.25], jointAxis = "1 0 0")
        
        # Wheel 3
        pyrosim.Send_Sphere(name="Wheel3", pos=[0,0,-0.5] , size=[0.5])
        
        pyrosim.End()

        # pyrosim.Start_URDF("bodyB.urdf")
        # pyrosim.Send_Cube(name="BodyB3x2", pos=[5,5,0.5] , size=[3,2,0.5])
        # pyrosim.Send_Joint(name = "BodyB3x2_BodyB1x4" , parent= "BodyB3x2" , child = "BodyB1x4" , type = "fixed", position = [-6.5,-6,0.5], jointAxis = "1 0 0")
        # pyrosim.Send_Cube(name="BodyB1x4", pos=[0,0,0] , size=[1,4,0.5])
        # pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Wheel2")

        pyrosim.Send_Motor_Neuron( name = 1 , jointName = "Link1_Wheel1")
        pyrosim.Send_Motor_Neuron( name = 2 , jointName = "Link3_Wheel3")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numMotorNeurons , weight = self.weights[currentRow][currentColumn])
        
        pyrosim.End()