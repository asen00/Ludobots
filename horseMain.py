from horseSimulation import SIMULATION
import os
import numpy as np
import random as rd

np.random.seed(0)
rd.seed(0)

os.system("rm horse.urdf")
sim = SIMULATION([0,0,5])
sim.Run()