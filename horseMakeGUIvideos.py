import os
import numpy as np
import time
import constants as c

timestamp = '02-27-23_13:21:17'
IDsForGUIvideos = np.load('IDforGUIvidoes_'+timestamp+'.npy')
os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python horseSimulate.py " + " GUI " + IDsForGUIvideos[0] + " 2>&1 &")
os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python horseSimulate.py " + " GUI " + IDsForGUIvideos[1] + " 2>&1 &")