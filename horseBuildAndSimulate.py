from horseSimulation import SIMULATION
from horsePHC import HORSE_PHC
import sys
import pickle
import constants as c

directOrGUI = sys.argv[1]
indexToShow = int(sys.argv[2])
timestamp = sys.argv[3]
seed = sys.argv[4]
gen = sys.argv[5]

def Unpickle(timestamp, seed, generation):
    with open('Checkpoints/checkpoint_'+timestamp+'_seed'+seed+'_gen'+str(generation)+'.pickle', 'rb') as handle:
            return pickle.load(handle)

## These are both self.parents dictionaries that are indexed by population member
gen0popForSeed = Unpickle(timestamp, seed, 0)
genLASTpopForSeed = Unpickle(timestamp, seed, c.numberofGenerations-1)

gen0popForSeed[indexToShow].Generate_Body()
gen0popForSeed[indexToShow].Generate_Brain()

genLASTpopForSeed[indexToShow].Generate_Body()
genLASTpopForSeed[indexToShow].Generate_Brain()

if gen == 'FIRST':
    gen0sim = SIMULATION(directOrGUI, gen0popForSeed[indexToShow].myID)
    gen0sim.Run()
else:
    genLASTsim = SIMULATION(directOrGUI, genLASTpopForSeed[indexToShow].myID)
    genLASTsim.Run()