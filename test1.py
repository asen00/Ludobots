import pybullet as p
import time

physicsClient = p.connect(p.GUI)
for i in range(1000):
    p.stepSimulation()
    print(i)
    t=1/60
    time.sleep(t)

p.disconnect(p.GUI)