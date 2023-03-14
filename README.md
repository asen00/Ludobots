# Random 3D Creature

## Introduction
Created using [Ludobots course](https://www.reddit.com/r/ludobots/wiki/installation/).

## About the Assignment
This robot has been evolved in such a way that its morphology mutates alongside its neural network. This is achieved using the following logic.
![IMG_0377](https://user-images.githubusercontent.com/114432525/221763804-8e41a558-64a0-4e05-831e-9af12cc36684.jpg)

For reference, links with sensors are colored green, those without are blue, and there is a blue world element present.

## How It Was Made
The root robot is a chain of 3 sensors, all joined together along the x-axis using 'revolute' joints; these will be referred to as thoraxes. Then, each link in the main body is given a random choice to either spawn a limb or not. If a limb is to be spawned, the number of sub-limbs, or "phalanges," is randomly chosen in the range 1-3. The limb may only propagate along the y- or z-axes.

Also mutated during evolution are the sensing capabilities of each phalange, the size of each phalange, adding phalanges to the end of limbs which have less than 3 phalanges (or to thoraxes with no limbs); changing sensing and adding phalanges also changes the neural network by adding/removing sensors/motors. The neural network is also independently mutated by changing synaptic weights of sensor-motor connections.

The robot was trained to move with a fitness function that maximizes x-distance of the root link from the origin.
![FinalEvolutionPlot](https://user-images.githubusercontent.com/114432525/225141952-77b8ac08-95ec-4113-bdd5-f411e02eaab1.png)

## Simulating Evolution

### Generating a Random Parent and the Genotype-to-Phenotype Map
### Spawning Children
### Mutating Bodies, Brains, or Both?
### Defining and Evaluating Fitness
### Creating Selection Pressue

## Tracking Evolution
Evolution is tracked using a fitness-vs.-generation graph. For each random seed in the range 1-5, a line is drawn to show the fittest population member in each generation. Below are some examples of plots produced.
<img width="998" alt="Screen Shot 2023-02-27 at 11 49 32 PM" src="https://user-images.githubusercontent.com/114432525/221765833-f5283964-51cf-4801-8094-d6b6b299ee2d.png">
<img width="996" alt="Screen Shot 2023-02-27 at 11 49 42 PM" src="https://user-images.githubusercontent.com/114432525/221765861-5a20bd4e-69b2-4f66-ae3f-671566e696e0.png">
<img width="996" alt="Screen Shot 2023-02-27 at 11 49 53 PM" src="https://user-images.githubusercontent.com/114432525/221765882-a756074e-0891-4f08-ab30-461ba22c660e.png">

However, to actually watch the evolution of a robot, one may use the file "horseMakeGUIvideos.py" to run GUI simulations of the first and last generations of the ending fittest member for any seed they specify. Below is an example of such evolution. This corresponds to the [last graph shown above](https://youtu.be/godZyfXm44s).

## Trends in Evolution

### Insights about Simultaneous Evolution of Brains and Bodies
