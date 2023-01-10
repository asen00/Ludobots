import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
#pyrosim.Send_Cube(name="Box1", pos=[0,0,0] , size=[1,1,1])
#pyrosim.Send_Cube(name="Box2", pos=[0,0,0] , size=[1,1,1])

for i in range(5):
    for j in range(5):
        for k in range(10):
            sz = 1*(1-(k/10))
            pyrosim.Send_Cube(name="Box", pos=[i,j,sz] , size=[1-sz,1-sz,1-sz])

pyrosim.End()