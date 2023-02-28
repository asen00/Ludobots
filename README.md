# Random 3D Creature

## Introduction
Created using [Ludobots course](https://www.reddit.com/r/ludobots/wiki/installation/).

## About the Assignment
This robot has been evolved in such a way that its morphology mutates alongside its neural network. This is achieved using the following logic.
![IMG_0377](https://user-images.githubusercontent.com/114432525/221763804-8e41a558-64a0-4e05-831e-9af12cc36684.jpg)

For reference, links with sensors are colored green, those without are blue, and there is a blue world element present.

## How It Was Made
The root robot is a chain of 5 sensors, all joined together along the x-axis using 'revolute' joints. Then, each link in the main body is given a random choice to either spawn a limb or not. If a limb is to be spawned, the number of sub-limbs, or "phalanges," is randomly chosen in the range 1-4. The limb may only propagate along the y- or z-axes, but can form in just one or both (positive and negative) directions along its chosen axis.

Also mutated during evolution are the sensing capabilities of each phalange, the axis of each revolving phalange joint, and the synaptic structure and weights of all the neurons.

The robot was trained to move in a straight line.

### New Skills Learned
1) [Random seed](https://www.analyticsvidhya.com/blog/2021/12/what-does-numpy-random-seed-do/)
In order to make the work reproducible, runs were indexed using random seeds 0-4. This means that if the code is rerun for a specific seed, it should produce the same solution since all random mutations will be re-picked in the same pseudorandom sequence.

2) [Checkpointing](https://legacy.docs.greatexpectations.io/en/stable/guides/how_to_guides/validation/how_to_run_a_checkpoint_in_python.html)
Since this program now needs to run for much longer timescales, checkpointing helped me store my place in the algorithm so that if the code crashed or needed to be stopped, the program could resume where it left off.

3) [Pickling](https://www.geeksforgeeks.org/understanding-python-pickling-example/)
I checkpointed using [Python's pickle module](https://docs.python.org/3/library/pickle.html).

## Seeing Evolution
Evolution is tracked using a fitness-vs.-generation graph. For each random seed in the range 1-5, a line is drawn to show the fittest population member in each generation. Below are some examples of plots produced.
<img width="998" alt="Screen Shot 2023-02-27 at 11 49 32 PM" src="https://user-images.githubusercontent.com/114432525/221765833-f5283964-51cf-4801-8094-d6b6b299ee2d.png">
<img width="996" alt="Screen Shot 2023-02-27 at 11 49 42 PM" src="https://user-images.githubusercontent.com/114432525/221765861-5a20bd4e-69b2-4f66-ae3f-671566e696e0.png">
<img width="996" alt="Screen Shot 2023-02-27 at 11 49 53 PM" src="https://user-images.githubusercontent.com/114432525/221765882-a756074e-0891-4f08-ab30-461ba22c660e.png">

However, to actually watch the evolution of a robot, one may use the file "horseMakeGUIvideos.py" to run GUI simulations of the first and last generations of the ending fittest member for any seed they specify. Below is an example of such evolution. This corresponds to the [last graph shown above](https://youtu.be/godZyfXm44s).

## Bugs
There is still one bugs remaining. The Construct_Limb() method in the HORSE_INFO class is still making my limbs grow into each other, and sometimes disjointed. This is affecting the way that the fitness is being written, and thus the robots are sometimes great at forward locomotion, and other times just move in circles.
