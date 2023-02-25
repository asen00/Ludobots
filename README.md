# Random 3D Creature

## Introduction
Created using [Ludobots course](https://www.reddit.com/r/ludobots/wiki/installation/).

## About the Assignment
This is a fully random robot, i.e., the number of links it has, their sizes, and their ability to sense their surroundings are generated using the [numpy.random.random()](https://numpy.org/doc/stable/reference/random/generated/numpy.random.random.html) and [random.randint()](https://www.w3schools.com/python/ref_random_randint.asp) functions. 

For reference, links with sensors are colored green, those without are blue, and there is a blue world element present.

## How It Was Made
I used object classes to store information about each link and then passed these attributes to [pyrosim](https://github.com/jbongard/pyrosim), which then called [pybullet](https://pybullet.org/wordpress/) functions.

To mitigate self-collisions, the method horseInfo.Constuct_Limb() was supposed to sprout limbs in a continuous fashion in the direction of limb growth. However, I think there is a tiny bug here which is making my joints form from within the previous link. It is also causing certain links to be spaced out more than they should be. I really have no idea if the bug is in my code or my logic. (I have tried debugging this one method for 4 hours and am not sure how to proceed.) Below is an image of the logic I was trying to follow.
![IMG_0338](https://user-images.githubusercontent.com/114432525/220254009-0c9f87d3-f952-491c-b759-99d3a98829f8.PNG)

Other than this bug, my robot is able to fill 3D space completely randomly, has randomly-assigned weights in its functional neural network, and has a class heirarchy which will hillclimbing and parallelization.

## Relevant Files
All the files related to this project have the prefix "horse", e.g. "horseJoint.py". To run the code, please use "horseMain.py". You can find a teaser for some results on [YouTube](https://youtu.be/02n35ynfyms).
