from horseSearch import EVOLUTION_TRACKER
import os

os.system("rm EvolutionPlot.png")
os.system("rm fullFitnessArray.npy")

evo = EVOLUTION_TRACKER(numRuns=5, checkpointGen=2)
evo.Run_Search()
evo.Plot_Evolution()