import numpy as np

## Number of iterations in simulation
num = 10000

## Number of hillclimbers
populationSize = 8

## Number of generations
numberofGenerations = 20

## Number of neurons
numSensorNeurons = 4
numMotorNeurons = 8

## Range of oscillatory motion on motors
motorJointRange = 0.2

## Sinusoidal control of leg motors
amplitude = np.pi/4
frequency = 6
phase = 0
maxForce = 50