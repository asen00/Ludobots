import pybullet as p
import pybullet_data
import time
import constants as c

from horseRobot import ROBOT
from world import WORLD

class SIMULATION:
    def __init__(self, origin):
        self.physicsClient = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.snake = ROBOT(self.world, origin)

    def Run(self):
        for timeStep in range(c.num):
            p.stepSimulation()
            self.snake.Sense(timeStep)
            self.snake.Think()
            #self.snake.Act(self.snake.robotId, timeStep)

            t=1/3000
            time.sleep(t)
    
    def __del__(self):
        # Uncomment if you want to save sensor/motor values
        #self.robot.sensors.Save_Values()
        #self.robot.motors.Save_Values()

        p.disconnect()