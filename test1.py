import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
from simulation import SIMULATION
from robot import ROBOT

simulation = SIMULATION()
SIMULATION.Run(ROBOT.robotId)

'''np.save("backsensorVals.npy", backLegSensorValues)
np.save("frontsensorVals.npy", frontLegSensorValues)'''