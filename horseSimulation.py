import pybullet as p
import pybullet_data
import time
import constants as c

from horseRobot import ROBOT
from world import WORLD

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI

        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT(solutionID, self.world)

    def Run(self):
        for timeStep in range(c.num):
            p.stepSimulation()
            self.robot.Sense(timeStep)
            self.robot.Think()
            self.robot.Act(self.robot.robotId, timeStep)

            t=1/3000
            if self.directOrGUI == "GUI":
                time.sleep(t)
    
    def Get_Fitness(self):
        self.robot.Get_Fitness()
    
    def __del__(self):
        # Uncomment if you want to save sensor/motor values
        #self.robot.sensors.Save_Values()
        #self.robot.motors.Save_Values()

        p.disconnect()