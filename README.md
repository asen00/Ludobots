# Random Snake

## Introduction
Created using [Ludobots course](https://www.reddit.com/r/ludobots/wiki/installation/).

## About the Assignment
This is a fully random robot, i.e., the number of links it has, their sizes, and their ability to sense their surroundings are generated using the [numpy.random.random()](https://numpy.org/doc/stable/reference/random/generated/numpy.random.random.html) and [random.randint()](https://www.w3schools.com/python/ref_random_randint.asp) functions. 

For reference, links with sensors are colored green, those without are blue, and there is a blue world element present.

## How It Was Made
I used object classes to store information about each link and then passed these attributes to [pyrosim](https://github.com/jbongard/pyrosim), which then called [pybullet](https://pybullet.org/wordpress/) functions.

One of the biggest challenges was learning how to keep randomly-generated joints and links flush with each other. The image below shows the logic I followed to ensure jointed morphologies.
![IMG_0304](https://user-images.githubusercontent.com/114432525/218278297-89c89ccc-eff6-4dbe-afb5-6bc246cd1623.jpg)

## Relevant Files
All the files related to this project have the prefix "snake", e.g. "snakeJoint.py". To run the code, please use "snakeMain.py". You can find a teaser for some results on [YouTube](https://youtu.be/iKKsa0DjAUI).

## Ability for Expansion
Since I modeled my class heirarchy after the Ludobots course (linked above), I have room to expand into evolving this snake via random mutations.
