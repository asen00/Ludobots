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
        randomRow = rd.randint(0,c.numSensorNeurons-1)
        randomColumn = rd.randint(0,c.numMotorNeurons-1)
        self.weights[randomRow, randomColumn] = rd.random() * 2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[0,3,0.5] , size=[1,1,1])
        pyrosim.End()

    '''def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1] , size=[1,1,1])
        
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0] , size=[0.2,1,0.2])
        pyrosim.Send_Joint(name = "FrontLeg_LowerFrLeg" , parent= "FrontLeg" , child = "LowerFrLeg" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerFrLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0,-0.5,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0] , size=[0.2,1,0.2])
        pyrosim.Send_Joint(name = "BackLeg_LowerBaLeg" , parent= "BackLeg" , child = "LowerBaLeg" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LowerBaLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        
        pyrosim.Send_Joint(name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [0.5,0,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[0.5,0,0] , size=[1,0.2,0.2])
        pyrosim.Send_Joint(name = "LeftLeg_LowerLeLeg" , parent= "LeftLeg" , child = "LowerLeLeg" , type = "revolute", position = [1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LowerLeLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])
        
        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [-0.5,0,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[-0.5,0,0] , size=[1,0.2,0.2])
        pyrosim.Send_Joint(name = "RightLeg_LowerRiLeg" , parent= "RightLeg" , child = "LowerRiLeg" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LowerRiLeg", pos=[0,0,-0.5] , size=[0.2,0.2,1])

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")
        
        # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "FrontLeg")
        # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "BackLeg")
        # pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        # pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")
        # pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "LowerFrLeg")
        # pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "LowerBaLeg")
        # pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LowerLeLeg")
        # pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "LowerRiLeg")

        # pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_FrontLeg")
        # pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_BackLeg")
        # pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Torso_LeftLeg")
        # pyrosim.Send_Motor_Neuron( name = 12 , jointName = "Torso_RightLeg")
        # pyrosim.Send_Motor_Neuron( name = 13 , jointName = "FrontLeg_LowerFrLeg")
        # pyrosim.Send_Motor_Neuron( name = 14 , jointName = "BackLeg_LowerBaLeg")
        # pyrosim.Send_Motor_Neuron( name = 15 , jointName = "LeftLeg_LowerLeLeg")
        # pyrosim.Send_Motor_Neuron( name = 16 , jointName = "RightLeg_LowerRiLeg")

        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "LowerFrLeg")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LowerBaLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LowerLeLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LowerRiLeg")

        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "FrontLeg_LowerFrLeg")
        pyrosim.Send_Motor_Neuron( name = 5 , jointName = "BackLeg_LowerBaLeg")
        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "LeftLeg_LowerLeLeg")
        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "RightLeg_LowerRiLeg")
        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Torso_RightLeg")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numMotorNeurons , weight = self.weights[currentRow][currentColumn])
        
        pyrosim.End()'''    
    
    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        
        # Link 1
        pyrosim.Send_Cube(name="Link1", pos=[0,0,2.25] , size=[3,2,0.5])

        # Leg 1
        pyrosim.Send_Joint(name = "Link1_Leg1Upper" , parent= "Link1" , child = "Leg1Upper" , type = "revolute", position = [-1.5,0,2.25], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg1Upper", pos=[0,0,-0.5] , size=[0.5,0.5,1])
        pyrosim.Send_Joint(name = "Leg1Upper_Leg1Lower" , parent= "Leg1Upper" , child = "Leg1Lower" , type = "revolute", position = [0,0,-1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg1Lower", pos=[0,0,-0.5] , size=[0.3,0.3,1])

        # Link 2
        pyrosim.Send_Joint(name = "Link1_Link2" , parent= "Link1" , child = "Link2" , type = "fixed", position = [1.5,0,2.25], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Link2", pos=[0.125,-0.125,0], size=[0.25,1.75,0.5])

        # Tracker
        pyrosim.Send_Joint(name = "Link2_Tracker" , parent= "Link2" , child = "Tracker" , type = "fixed", position = [0.125,0.75,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Tracker", pos=[0,0.125,0], size=[0.25,0.25,0.5])
        
        # Link 3
        pyrosim.Send_Joint(name = "Link2_Link3" , parent= "Link2" , child = "Link3" , type = "fixed", position = [0.25,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Link3", pos=[0.5,1,0] , size=[1,4,0.5])
        
        # Leg 2
        pyrosim.Send_Joint(name = "Link3_Leg2Upper" , parent= "Link3" , child = "Leg2Upper" , type = "revolute", position = [1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg2Upper", pos=[0,0,-0.5] , size=[0.5,0.5,1])
        pyrosim.Send_Joint(name = "Leg2Upper_Leg2Lower" , parent= "Leg2Upper" , child = "Leg2Lower" , type = "revolute", position = [0,0,-1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg2Lower", pos=[0,0,-0.5] , size=[0.3,0.3,1])

        # Leg 3
        pyrosim.Send_Joint(name = "Link3_Leg3Upper" , parent= "Link3" , child = "Leg3Upper" , type = "revolute", position = [1,2,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg3Upper", pos=[0,0,-0.5] , size=[0.5,0.5,1])
        pyrosim.Send_Joint(name = "Leg3Upper_Leg3Lower" , parent= "Leg3Upper" , child = "Leg3Lower" , type = "revolute", position = [0,0,-1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg3Lower", pos=[0,0,-0.5] , size=[0.3,0.3,1])

        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain"+str(self.myID)+".nndf")
        
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Leg1Lower")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Leg2Lower")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Leg3Lower")

        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Link1_Leg1Upper")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Leg1Upper_Leg1Lower")
        pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Link3_Leg2Upper")
        pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Leg2Upper_Leg2Lower")
        pyrosim.Send_Motor_Neuron( name = 7 , jointName = "Link3_Leg3Upper")
        pyrosim.Send_Motor_Neuron( name = 8 , jointName = "Leg3Upper_Leg3Lower")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numMotorNeurons , weight = self.weights[currentRow][currentColumn])
        
        pyrosim.End()