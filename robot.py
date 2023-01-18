import pybullet as p
import pyrosim.pyrosim as pyrosim

from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self):
        self.sensors = {}
        self.motors = {}

        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
    
    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, timeStep):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(timeStep)
    
    def Act(self, robotId, timeStep):
        for motor in self.motors:
            self.motors[motor].Set_Value(robotId, timeStep)