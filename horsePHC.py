from horse import HORSE_SOLUTION
import constants as c
import numpy as np
import random as rd
import copy
import os
import pickle

class HORSE_PHC:
    def __init__(self, randomseed, timestamp):        
        os.system("rm miscStorage/horse*.nndf")
        os.system("rm miscStorage/horse*.urdf")
        os.system("rm miscStorage/HORSEfitness*.txt")
        
        self.seed = randomseed
        np.random.seed(randomseed)
        rd.seed(randomseed)

        self.timestamp = timestamp

        self.parents = {}

        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = HORSE_SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve_and_Save_Fitness_and_Checkpoint(self, pergen):
        self.Evaluate(self.parents)

        self.fitnessAllGen = np.zeros((c.numberofGenerations, c.populationSize))
        self.checkpointParents = {}
        for currentGeneration in range(c.numberofGenerations):
            self.Evolve_For_One_Generation()
            self.Save_Fitness(currentGeneration)
            self.Checkpoint(currentGeneration, pergen)
    
    def Save_Fitness(self, generation):
        self.fitnessAllGen[generation] = self.Return__Population_Fitness_for_Generation()
    
    def Checkpoint(self, generation, pergen):
        if (generation == 0) or (generation % pergen == 0) or (generation == c.numberofGenerations-1):
                self.checkpointParents[generation] = self.parents
                self.Pickle_Checkpoints(generation)

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

    def Pickle_Checkpoints(self, generation):
        with open('Checkpoints/checkpoint_'+self.timestamp+'_seed'+str(self.seed)+'_gen'+str(generation)+'.pickle', 'wb') as handle:
            pickle.dump(self.checkpointParents[generation], handle, protocol=pickle.HIGHEST_PROTOCOL)

    def Unpickle_Checkpoints(self, generation):
        with open('Checkpoints/checkpoint_'+self.timestamp+'_seed'+str(self.seed)+'_gen'+str(generation)+'.pickle', 'rb') as handle:
            return pickle.load(handle)