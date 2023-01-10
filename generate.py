import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
#pyrosim.Send_Cube(name="Box1", pos=[0,0,0] , size=[1,1,1])
#pyrosim.Send_Cube(name="Box2", pos=[0,0,0] , size=[1,1,1])
for j in range(5):
    for k in range(5):
        for i in range(10):
            side = 1*(1-(i/10))
            pyrosim.Send_Cube(name="Box1", pos=[j,k,side] , size=[1-side,1-side,1-side])

pyrosim.End()