import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random as rd
import constants as c

pass

'''physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
robotId = p.loadURDF("body.urdf")
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)'''

'''backLegSensorValues = np.zeros(c.num)
frontLegSensorValues = np.zeros(c.num)'''

'''x = np.linspace(0, 2*np.pi, c.num)

backAngles = c.backAmp * np.sin(c.backFreq * x + c.backPhase) + c.backConst
frontAngles = c.frontAmp * np.sin(c.frontFreq * x + c.frontPhase) + c.frontConst'''

'''for i in range(c.num):
    p.stepSimulation()
    backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    backLegSensorValues[i] = backLegTouch
    frontLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
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
    
    t=1/240
    time.sleep(t)'''

'''p.disconnect()

np.save("backsensorVals.npy", backLegSensorValues)
np.save("frontsensorVals.npy", frontLegSensorValues)'''