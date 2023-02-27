from horse import HORSE_SOLUTION
import constants as c
import numpy as np
import copy
import os
import pickle

class HORSE_PHC:
    def __init__(self, randomseed):
        os.system("rm horse*.nndf")
        os.system("rm horse*.urdf")
        os.system("rm HORSEfitness*.txt")
        
        self.seed = randomseed
        np.random.seed(randomseed)

        self.parents = {}

        self.nextAvailableID = 0

        for i in range(c.populationSize):
            self.parents[i] = HORSE_SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)

        self.fitnessAllGen = np.zeros((c.numberofGenerations, c.populationSize))
        for currentGeneration in range(c.numberofGenerations):
            self.Evolve_For_One_Generation()
            self.fitnessAllGen[currentGeneration] = self.Return__Population_Fitness_for_Generation()
    
    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        #self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i in range(c.populationSize):
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Mutate(self):
        for i in range(c.populationSize):
            self.children[i].Mutate()
    
    def Evaluate(self, solutions):
        for i in range(c.populationSize):
            solutions[i].Start_Simulation("DIRECT")
        
        for i in range(c.populationSize):
            solutions[i].Wait_For_Simulation_To_End()

    def Print(self):
        for i in range(c.populationSize):
            print("Robot", i, "\n Parent fitness: ", self.parents[i].fitness, " Child fitness: ", self.children[i].fitness, "\n")
    
    def Select(self):
        for popMember in range(c.populationSize):
            if self.parents[popMember].fitness < self.children[popMember].fitness:
                self.parents[popMember] = self.children[popMember]
    
    def Return__Population_Fitness_for_Generation(self):
        popFitnessForGen = np.zeros(c.populationSize)
        for popMember in range(c.populationSize):
            popFitnessForGen[popMember] = self.parents[popMember].fitness
        return popFitnessForGen

    def Show_Best_and_Checkpoint_and_Get_Fitness_File(self, pergen):
        popFitnesses = np.zeros(c.populationSize)
        for i in range(c.populationSize):
            popFitnesses[i] = self.parents[i].fitness
        
        self.checkpointParents = {}
        for gen in range(c.numberofGenerations):
            if (gen == 0) or (gen % pergen == 0) or (gen == c.numberofGenerations-1):
                self.checkpointParents[gen] = self.parents[np.argmax(popFitnesses)]
                self.Pickle_Checkpoints(gen)

        self.parents[0].Start_Simulation("GUI")
        self.parents[np.argmax(popFitnesses)].Start_Simulation("GUI")

        return self.fitnessAllGen

    def Pickle_Checkpoints(self, generation):
        with open('checkpoints_seed'+str(self.seed)+'_gen'+str(generation)+'.pickle', 'wb') as handle:
            pickle.dump(self.checkpointParents[generation], handle, protocol=pickle.HIGHEST_PROTOCOL)

    def Unpickle_Checkpoints(self, generation):
        with open('checkpoints_seed'+str(self.seed)+'_gen'+str(generation)+'.pickle', 'rb') as handle:
            return pickle.load(handle)