import numpy as np
import matplotlib.pyplot as plt
import constants as c

fullfitnessArray = np.load('Outputs/fullfitnessArray_03-12-23_21:44:19.npy')

x = np.arange(c.numberofGenerations)
        
fittestMember = np.zeros((10, c.numberofGenerations))
        
color_dict = {0:'#EB4034', 1:'#EB9B34', 2:'#EBE01E', 3:'#7FD141', 4:'#2AD1D4', 5:'#1109ED', 6:'k', 7:'#C479F2', 8:'#D42AC0', 9:'#F2798F'}

for seed in range(10):
    #plt.plot(x, fullfitnessArray[seed], linestyle='', marker="o", color=color_dict[seed], markersize=0.5)
    for gen in range(c.numberofGenerations):
        fittestMember[seed][gen] = fullfitnessArray[seed][gen][np.argmax(fullfitnessArray[seed][gen])]
    plt.plot(x, fittestMember[seed], linestyle='-', label='Run:'+str(seed), color=color_dict[seed])

plt.xticks(np.arange(0, c.numberofGenerations+1, c.numberofGenerations/10))
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend(prop={'size': 8})
plt.savefig('Outputs/FinalEvolutionPlot.png', dpi=600)
plt.show()