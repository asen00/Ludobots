from horseSimulation import SIMULATION
import os

os.system("rm horse.urdf")
sim = SIMULATION([0,0,5])
sim.Run()