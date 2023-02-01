import pyrosim.pyrosim as pyrosim
import numpy as np
import random as rd
import time
import os

class SOLUTION:
    def __init__(self, ID):        
        self.weights = (2*np.random.rand(3,2))-1

        self.myID = str(ID)

    def Set_ID(self, childID):
        self.myID = str(childID)

    def Start_Simulation(self, directOrGUI):
        self.Generate_Brain()
        os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python test1.py " + directOrGUI + " " + self.myID + " 2&>1 &")
    
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
        randomRow = rd.randint(0,2)
        randomColumn = rd.randint(0,1)
        self.weights[randomRow, randomColumn] = rd.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0,3,0.5] , size=[1,1,1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5] , size=[1,1,1])
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0.5,0,1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[1,1,1])
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [-0.5,0,1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[1,1,1])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")
        
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + 3 , weight = self.weights[currentRow][currentColumn])
        
        pyrosim.End()