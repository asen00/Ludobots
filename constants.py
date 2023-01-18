import numpy as np

## Number of iterations in simulation
num=10000

## Sinusoidal control of leg motors (Task G)

# Back Leg
backAmp = np.pi/24
backFreq = 6
backPhase = 0
backConst = np.pi/3

# Front Leg
frontAmp = np.pi/6
frontFreq = 6
frontPhase = 0
frontConst = 0