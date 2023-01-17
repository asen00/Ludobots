import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random as rd

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
robotId = p.loadURDF("body.urdf")
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

num=1000

backLegSensorValues = np.zeros(num)
frontLegSensorValues = np.zeros(num)

x = np.linspace(0, 2*np.pi, num)

backAmp = np.pi/24
backFreq = 6
backPhase = 0
backConst = np.pi/3

frontAmp = np.pi/6
frontFreq = 6
frontPhase = 0
frontConst = 0

backAngles = backAmp * np.sin(backFreq * x + backPhase) + backConst
frontAngles = frontAmp * np.sin(frontFreq * x + frontPhase) + frontConst

for i in range(num):
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
    time.sleep(t)

p.disconnect()

np.save("backsensorVals.npy", backLegSensorValues)
np.save("frontsensorVals.npy", frontLegSensorValues)