# Random 3D Creature

## Introduction
Created using [Ludobots course](https://www.reddit.com/r/ludobots/wiki/installation/).

## Simulating Evolution
To understand my process, you may either read the text here (which includes all the detail about genotypes, phenotypes, the evolutionary algorithm, etc.) or watch this [quick video](https://youtu.be/-bC79AYuqt0) (which includes B-roll).

### Generating a Random Parent and the Genotype-to-Phenotype Map
The root robot is a chain of 3 sensors, all joined together along the x-axis using 'revolute' joints; these will be referred to as thoraxes. Then, each link in the main body is given a random choice to either sprout a limb along one face, two faces, or not sprout limbs at all. If a limb is to be grown, the number of sub-limbs, or "phalanges," is randomly chosen in the range 1-3. Each phalange may choose to propagate in either the y- or z-directions and can revolve along the x-, y- or z-axis. Shown below is what would happen if each thorax decided to grow all 6 allowed phalanges.
![Add a heading](https://user-images.githubusercontent.com/114432525/225158691-816c48cc-aec3-40d2-94dd-b3f34bdab966.png)

However, since the robots are formed using direct encoding, there is no general formula for a genotype map, as there exists in recursive algorithms such as L-systems. Here, each thorax has options on the number of limbs to grow and each limb has a choice of number of phalanges. Thus, genotype maps become a case-by-case encoding of the robot’s body. Consider another example.
![Add a heading-2](https://user-images.githubusercontent.com/114432525/225158741-a4c94f2d-f81d-4443-b12b-fbbbd7725e90.png)

Finally, let’s consider the brains of these robots. How are they generated? First, each link (thorax and phalange) is assigned a bit that either turns on its touch sensing capability or lets the sensor remain dormant. Then, a simple network connects every sensor to every revolving motorized joint, each connection having some random synaptic weight.
![Add a heading-3](https://user-images.githubusercontent.com/114432525/225158781-e0b9df7f-f25d-4215-ae37-f27a03aa36fb.png)

### Spawning Children
Spawning a child is just creating a copy of the parent’s genotype and then using it to build an identical robot.

### Mutating Bodies, Brains, or Both?
First, the robot’s body is mutated. This can be done in one of three ways:
Changing the size of a phalange
Changing the sensing capability of a phalange
Adding a phalange to a limb with less than 3 phalanges (or to a thorax with no limbs).
The choice of which phalange/limb to change, the change to be made, and the new value of the chosen parameter are all determined randomly. Note that either the second or third option also involve changing the neural network, i.e., adding/removing a sensor and/or a motor.

After the body has been changed, the synaptic weight of a random sensor-motor connection is assigned a new random value. This changes the performance of the neural network.

### Defining and Evaluating Fitness
The fitness of each robot is calculated and stored. These robots were trained to move using a fitness function that maximizes x-distance of the root link from the origin.

### Creating Selection Pressure
At each generation, the best robot is selected for using the following algorithm. If the parent is fitter than the child, the child is deleted and the parent undergoes random mutation again. If the child is fitter than the parent, it becomes a parent and spawns a child of its own which then undergoes mutation.

The repetition of this over several generations forces only those which locomote to survive and phylogenetically propagate.

## Parallelization and Seeding
In order to better utilize computational resources, the evolutionary algorithm is parallelized, i.e., a population of 10 random parents are allowed to evolve simultaneously. At the end of 500 generations, the fittest population member is selected. This decreases the time to evaluate 5000 simulations since we are no longer just searching the space sequentially.

Finally, the functionality of this algorithm needs to be tested. We do this by setting random seeds such that the evolutionary choices made at each iteration can be repeated if the process is initialized with the same seed. Seeds 0-9 were used to see whether this evolutionary algorithm was actually making robots fitter, or whether it was just happening by chance.

## Tracking Evolution
Evolution is tracked using a fitness-vs.-generation graph. For each random seed 0-9, a line is drawn to show the fittest population member in each generation. 
![FinalEvolutionPlot](https://user-images.githubusercontent.com/114432525/225159746-c68eaf17-1e53-4dd3-a04a-5dac6ce5589a.png)

To watch the evolution of a robot, one may use the file "horseMakeGUIvideos.py" to run GUI simulations of the first and last generations of the ending fittest member for any seed they specify. [Here is an example of such evolution for seed 6.](https://youtu.be/f34L5RC4C8k)

## Trends in Evolution

### Insights about Simultaneous Evolution of Brains and Bodies

## How to Run the Code
The evolutionary algorithm is run through horsePlotSearch.py and once finished, the robot for any specified run can be watched by pasting the starting timestamp (printed) into horseMakeGUIvideos.py and running this file.
