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

num=10000

backLegSensorValues = np.zeros(num)
frontLegSensorValues = np.zeros(num)

x = np.linspace(0, 2*np.pi, num)
targetAngles = np.sin(x)
np.save("sinplotTest.npy", targetAngles)
exit()

for i in range(num):
    p.stepSimulation()
    backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    backLegSensorValues[i] = backLegTouch
    frontLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    frontLegSensorValues[i] = frontLegTouch
    
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, 
                                jointName = 'Torso_BackLeg', 
                                controlMode = p.POSITION_CONTROL,
                                targetPosition = rd.random()*(-np.pi/4.0),
                                maxForce = 30)

    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, 
                                jointName = 'Torso_FrontLeg', 
                                controlMode = p.POSITION_CONTROL,
                                targetPosition = rd.random()*(np.pi/4.0),
                                maxForce = 30)
    
    t=1/60
    time.sleep(t)

p.disconnect()

np.save("backsensorVals.npy", backLegSensorValues)
np.save("frontsensorVals.npy", frontLegSensorValues)