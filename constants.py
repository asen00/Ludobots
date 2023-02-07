import numpy as np

## Number of iterations in simulation
num = 10000

## Number of hillclimbers
populationSize = 1

## Number of generations
numberofGenerations = 3

## Number of neurons
numSensorNeurons = 1
numMotorNeurons = 2

## Range of oscillatory motion on motors
motorJointRange = 360

## Sinusoidal control of leg motors
amplitude = np.pi/4
frequency = 6
phase = 0
maxForce = 50