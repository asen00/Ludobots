import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backsensorVals.npy")
frontLegSensorValues = np.load("data/frontsensorVals.npy")
plt.plot(backLegSensorValues, label="Back Leg", linestyle="--")
plt.plot(frontLegSensorValues, label="Front Leg", linestyle="--")
plt.legend()
plt.title("Sensor Values")
plt.savefig("sensorvals.png", dpi=300)
plt.show()