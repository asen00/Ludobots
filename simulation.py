import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy as np
import constants as c

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self):        
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        '''x = np.linspace(0, 2*np.pi, c.num)

        backAngles = c.backAmp * np.sin(c.backFreq * x + c.backPhase) + c.backConst
        frontAngles = c.frontAmp * np.sin(c.frontFreq * x + c.frontPhase) + c.frontConst'''
        
        for timeStep in range(c.num):
            p.stepSimulation()
            ROBOT.Sense(self, timeStep)

            t=1/60
            time.sleep(t)

            '''
            backLegSensorValues[i] = backLegTouch
            frontLegSensorValues[i] = frontLegTouch
            
            pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, 
                                        jointName = 'Torso_BackLeg', 
                                        controlMode = p.POSITION_CONTROL,
                                        targetPosition = backAngles[i],
                                        maxForce = 30)

            pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, 
                                        jointName = 'Torso_FrontLeg', 
                                        controlMode = p.POSITION_CONTROL,
                                        targetPosition = frontAngles[i],
                                        maxForce = 30)
            
            '''
    
    def __del__(self):
        p.disconnect()