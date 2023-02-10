from snakeSimulation import SIMULATION
import os

os.system("rm snake.urdf")
sim = SIMULATION([0,0,5])
sim.Run()