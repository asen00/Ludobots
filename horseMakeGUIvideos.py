import os
import numpy as np

timestamp = '03-12-23_21:44:19'
run = 6
IDsForGUIvideos = np.load('Outputs/IDforGUIvidoes_'+timestamp+'.npy')

os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python horseBuildAndSimulate.py " + " GUI " + str(IDsForGUIvideos[run]) + " " + timestamp + " " + str(run) + " FIRST" + " 2>&1 &")
os.system("/Users/AntaraSen_1/opt/anaconda3/bin/python horseBuildAndSimulate.py " + " GUI " + str(IDsForGUIvideos[run]) + " " + timestamp + " " + str(run) + " LAST" + " 2>&1 &")