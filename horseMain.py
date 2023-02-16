from horseSimulation import SIMULATION
import os

os.system("rm horse.urdf")
sim = SIMULATION([0,0,0])
sim.Run()