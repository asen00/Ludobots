from horsePHC import HORSE_PHC
import numpy as np
import constants as c
import matplotlib.pyplot as plt
import random as rd
import os

class EVOLUTION_TRACKER:
    def __init__(self, numRuns, checkpointGen, timestamp):
        os.system("rm checkpoint*.pickle")

        self.numRuns = numRuns
        self.checkpointGen = checkpointGen
        self.timestamp = timestamp

    def Run_Search(self):
        self.phc = {}
        self.fullfitnessArray = np.zeros((self.numRuns, c.numberofGenerations, c.populationSize))
        for seed in range(self.numRuns):
            self.phc[seed] = HORSE_PHC(seed, self.timestamp)
            self.phc[seed].Evolve_and_Save_Fitness_and_Checkpoint(self.checkpointGen)
            self.fullfitnessArray[seed] = self.phc[seed].fitnessAllGen
        
        np.save('fullfitnessArray_'+self.timestamp+'.npy', self.fullfitnessArray)
    
    def Plot_Evolution(self):
        x = np.arange(c.numberofGenerations)
        
        fittestMember = np.zeros((self.numRuns, c.numberofGenerations))
        
        color_dict = {0:'#E61717', 1:'#E69317', 2:'#56BF52', 3:'#5EC1F2', 4:'#9B43D1'}

        for seed in range(self.numRuns):
            plt.plot(x, self.fullfitnessArray[seed], linestyle='', marker="o", color=color_dict[seed], markersize=0.1)
            for gen in range(c.numberofGenerations):
                fittestMember[seed][gen] = self.fullfitnessArray[seed][gen][np.argmax(self.fullfitnessArray[seed][gen])]
            plt.plot(x, fittestMember[seed], linestyle='-', label='Run:'+str(seed), color=color_dict[seed])

        plt.xticks(x)
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.legend()
        plt.savefig('EvolutionPlot_'+self.timestamp+'.png', dpi=600)
        plt.show()
    
    def Save_Evolution_of_Fittest(self, randomSeed):
        fittestPopMemberGenLAST = np.argmax(self.fullfitnessArray[randomSeed][c.numberofGenerations-1])
        gen0PopMemberID = self.phc[randomSeed].Unpickle_Checkpoints(0)[fittestPopMemberGenLAST].myID
        genLASTPopMemberID = self.phc[randomSeed].Unpickle_Checkpoints(c.numberofGenerations-1)[fittestPopMemberGenLAST].myID
        np.save('IDforGUIvidoes_'+self.timestamp+'.npy', np.array([gen0PopMemberID, genLASTPopMemberID]))