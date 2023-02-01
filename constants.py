import numpy as np

## Number of iterations in simulation
num = 100

## Number of hillclimbers
populationSize = 1

## Number of generations
numberofGenerations = 1

## Number of neurons
numSensorNeurons = 3
numMotorNeurons = 2

## Sinusoidal control of leg motors
amplitude = np.pi/4
frequency = 6
phase = 0
maxForce = 50