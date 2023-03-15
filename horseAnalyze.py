from horseSimulation import SIMULATION
import pickle
import numpy as np

directOrGUI = 'GUI'
timestamp = '03-12-23_21:44:19'
seed = 3
gen = 10
IDsForGUIvideos = np.load('Outputs/IDforGUIvidoes_'+timestamp+'.npy')
indexToShow = IDsForGUIvideos[seed]

def Unpickle(timestamp, seed, generation):
    with open('Run03-12-23_21:44:19_Checkpoints/checkpoint_'+timestamp+'_seed'+str(seed)+'_gen'+str(generation)+'.pickle', 'rb') as handle:
            return pickle.load(handle)

robot = Unpickle(timestamp, seed, gen)

robot[indexToShow].Generate_Body()
robot[indexToShow].Generate_Brain()

sim = SIMULATION(directOrGUI, robot[indexToShow].myID)
sim.Run()