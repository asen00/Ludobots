import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
    
    def Set_Value(self, robotId, desiredAngle):
        self.motorForce = c.maxForce
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, 
                                    jointName = self.jointName, 
                                    controlMode = p.POSITION_CONTROL,
                                    targetPosition = desiredAngle,
                                    maxForce = self.motorForce)