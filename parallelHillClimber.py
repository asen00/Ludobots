from solution import SOLUTION
import constants as c
import numpy as np
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        
        self.parents = {}

        self.nextAvailableID = 0

        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberofGenerations):
            self.Evolve_For_One_Generation("DIRECT")
    
    def Evolve_For_One_Generation(self, directOrGUI):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
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
        for i in range(c.populationSize):
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]
    
    def Show_Best(self):
        popFitnesses = np.zeros(c.populationSize)
        for i in range(c.populationSize):
            popFitnesses[i] = self.parents[i].fitness
        
        #print(np.max(popFitnesses))
        self.parents[np.argmin(popFitnesses)].Start_Simulation("GUI")