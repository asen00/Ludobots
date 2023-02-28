import os
import numpy as np
import time
import constants as c

timestamp = '02-27-23_22:45:34'
run = 1
IDsForGUIvideos = np.load('IDforGUIvidoes_'+timestamp+'.npy')
print(IDsForGUIvideos)
os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python horseSimulate.py " + " GUI " + str(IDsForGUIvideos[0][run]) + " 2>&1 &")
os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python horseSimulate.py " + " GUI " + str(IDsForGUIvideos[1][run]) + " 2>&1 &")