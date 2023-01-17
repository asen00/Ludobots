import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backsensorVals.npy")
frontLegSensorValues = np.load("data/frontsensorVals.npy")
plt.plot(backLegSensorValues, label="Back Leg")
plt.plot(frontLegSensorValues, label="Front Leg")
plt.legend()
plt.show()