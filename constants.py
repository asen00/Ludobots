import numpy as np
import random as rd

## Number of iterations in simulation
num = 10000

## Number of hillclimbers
populationSize = 1

## Number of generations
numberofGenerations = 10

## Number of neurons
numSensorNeurons = 3
numMotorNeurons = 6

## Range of oscillatory motion on motors
motorJointRange = 1

## Sinusoidal control of leg motors
amplitude = np.pi/4
frequency = 6
phase = 0
maxForce = 200