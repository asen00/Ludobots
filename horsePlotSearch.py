from horseSearch import EVOLUTION_TRACKER
import random as rd
import datetime as date
import constants as c

start = date.datetime.now().strftime("%m-%d-%y_%H:%M:%S")

numRuns = 5

evo = EVOLUTION_TRACKER(numRuns=numRuns, checkpointGen=5, timestamp=start)
evo.Run_Search()
evo.Plot_Evolution()
evo.Save_Evolution_of_Fittest()

end = date.datetime.now().strftime("%m-%d-%y_%H:%M:%S")

print("Start time: ", start)
print("End time: ", end)