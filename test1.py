import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
robotId = p.loadURDF("body.urdf")
planeId = p.loadURDF("plane.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

num=100

backLegSensorValues = np.zeros(num)
frontLegSensorValues = np.zeros(num)

for i in range(num):
    p.stepSimulation()
    backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    backLegSensorValues[i] = backLegTouch
    frontLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    frontLegSensorValues[i] = frontLegTouch
    t=1/60
    time.sleep(t)

p.disconnect()

np.save("backsensorVals.npy", backLegSensorValues)
np.save("frontsensorVals.npy", frontLegSensorValues)