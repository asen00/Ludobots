import pybullet as p
import pybullet_data
import time
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
        for timeStep in range(c.num):
            p.stepSimulation()
            self.robot.Sense(timeStep)
            self.robot.Act(self.robot.robotId, timeStep)

            t=1/60
            time.sleep(t)
    
    def __del__(self):
        # Uncomment if you want to save sensor/motor values
        #self.robot.sensors.Save_Values()
        #self.robot.motors.Save_Values()

        p.disconnect()