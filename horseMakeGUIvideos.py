import os
import numpy as np
import time
import constants as c

timestamp = '03-08-23_10:28:15'
run = 0
IDsForGUIvideos = np.load('Outputs/IDforGUIvidoes_'+timestamp+'.npy')

os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python horseBuildAndSimulate.py " + " GUI " + str(IDsForGUIvideos[run]) + " " + timestamp + " " + str(run) + " FIRST" + " 2>&1 &")
os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python horseBuildAndSimulate.py " + " GUI " + str(IDsForGUIvideos[run]) + " " + timestamp + " " + str(run) + " LAST" + " 2>&1 &")