import numpy as np
import matplotlib.pyplot as plt

targetAngles = np.load("data/sinplotTest.npy")
plt.plot(np.linspace(0, 2*np.pi, 10000), targetAngles)
plt.show()

backLegSensorValues = np.load("data/backsensorVals.npy")
frontLegSensorValues = np.load("data/frontsensorVals.npy")
plt.plot(backLegSensorValues, label="Back Leg", linestyle="--")
plt.plot(frontLegSensorValues, label="Front Leg", linestyle="--")
plt.legend()
plt.title("Sensor Values")
plt.savefig("sensorvals.png", dpi=300)
plt.show()