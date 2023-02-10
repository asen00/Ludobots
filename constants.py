import numpy as np
import random as rd

## Number of iterations in simulation
num = 10000

## Number of hillclimbers
populationSize = 6

## Number of generations
numberofGenerations = 30

## Number of neurons
numSensorNeurons = 3
numMotorNeurons = 6

## Range of oscillatory motion on motors
motorJointRange = 0.2

## Sinusoidal control of leg motors
amplitude = np.pi/4
frequency = 6
phase = 0
maxForce = 200

## Snake
numLinks = rd.randint(0,10)