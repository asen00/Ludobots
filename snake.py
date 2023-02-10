import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c

from snakeInfo import SNAKE_INFO

class SNAKE:
    def __init__(self):
        self.numLinks = c.numLinks
        self.info = SNAKE_INFO(self.numLinks)
        self.links = self.info.Get_Links()
        self.joints = self.info.Get_Joints()

    def Generate_Snake_Body(self):
        pyrosim.Start_URDF("snake.urdf")
        
        for i in range(self.numLinks):
            pyrosim.Send_Cube(name = str(i), pos = self.links[i].pos, size = self.links[i].size)
            pyrosim.Send_Joint(name = self.joints[i].jointName , parent= self.joints[i].parentLink , child = self.joints[i].childLink , type = "revolute", position = self.joints[i].pos, jointAxis = self.joints[i].jointAxis)
        
        pyrosim.End()