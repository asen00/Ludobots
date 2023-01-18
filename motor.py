import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()
    
    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.phase = c.phase
        
        x = np.linspace(0, 2*np.pi, c.num)

        if self.jointName == 'Torso_FrontLeg':
            self.motorValues = self.amplitude * np.sin(self.frequency * x + self.phase)
        else:
            self.motorValues = 10*self.amplitude * np.sin(10*self.frequency * x + self.phase)
    
    def Set_Value(self, robotId, timestep):
        self.motorForce = c.maxForce
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, 
                                    jointName = self.jointName, 
                                    controlMode = p.POSITION_CONTROL,
                                    targetPosition = self.motorValues[timestep],
                                    maxForce = self.motorForce)
    
    def Save_Values(self):
        np.save("motorVals.npy", self.motorValues)