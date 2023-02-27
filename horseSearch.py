from horsePHC import HORSE_PHC
import numpy as np
import constants as c
import matplotlib.pyplot as plt
import os

class EVOLUTION_TRACKER:
    def __init__(self, numRuns, checkpointGen):
        os.system("rm checkpoints*.pickle")

        self.numRuns = numRuns
        self.checkpointGen = checkpointGen

    def Run_Search(self):
        self.fullfitnessArray = np.zeros((self.numRuns, c.numberofGenerations, c.populationSize))
        for seed in range(self.numRuns):
            phc = HORSE_PHC(seed)
            phc.Evolve()
            self.fullfitnessArray[seed] = phc.Show_Best_and_Checkpoint_and_Get_Fitness_File(self.checkpointGen)
        
        np.save('fullfitnessArray.npy', self.fullfitnessArray)
    
    def Plot_Evolution(self):
        x = np.linspace(start=0, stop=c.numberofGenerations, num=c.numberofGenerations)
        
        fittestMember = np.zeros((self.numRuns, c.numberofGenerations))
        
        for seed in range(self.numRuns):
            plt.plot(x, self.fullfitnessArray[seed], linestyle='', marker="o", color=((30+(56*seed))/255, (168+(21*seed))/255, (131+(10*seed))/255))
            for gen in range(c.numberofGenerations):
                fittestMember[seed][gen] = self.fullfitnessArray[seed][gen][np.argmax(self.fullfitnessArray[seed][gen])]
            plt.plot(x, fittestMember[seed], linestyle='-', label='Run:'+str(seed), color=((30+(56*seed))/255, (168+(21*seed))/255, (131+(10*seed))/255))

        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.savefig('EvolutionPlot.png', dpi=600)
        plt.show()