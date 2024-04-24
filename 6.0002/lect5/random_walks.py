import math
import random


# Random Walks - Drunk Simulation 6.0002 Lecture 5
class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, delta_x, delta_y):
        """delta_x and delta_y are floats"""
        return Location(self.x + delta_x, self.y + delta_y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def distance_from(self, other):
        x_distance = self.x - other.get_x()
        y_distance = self.y - other.get_y()
        return math.sqrt(x_distance**2 + y_distance**2)

    def __str__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ">"


class Drunk:
    def __init__(self, name=None):
        """Assumes name is a str"""
        self.name = name

    def __str__(self):
        if self != None:
            return self.name
        return "Anonymous"

    def take_step(self):
        raise NotImplementedError("Please implement this method")


class UsualDrunk(Drunk):
    def take_step(self):
        step_choices = [(0.0, 1), (0.0, -1), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(step_choices)


class MasochistDrunk(Drunk):
    def take_step(self):
        step_choices = [(0.0, 1.1), (0.0, -0.9), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(step_choices)


class Field:
    def __init__(self):
        self.drunks = {}

    def add_drunk(self, drunk, location):
        if drunk in self.drunks:
            raise ValueError("Duplicate drunk")
        self.drunks[drunk] = location

    def get_location(self, drunk):
        if drunk not in self.drunks:
            raise ValueError("Drunk not in field")
        return self.drunks[drunk]

    def move_drunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError("Drunk not in field")
        x_dist, y_dist = drunk.take_step()
        # use move method of Location to get new location
        self.drunks[drunk] = self.drunks[drunk].move(x_dist, y_dist)


# Simulating a walk
def walk(field, drunk, num_steps):
    """Assumes: f a Field, d a Drunk in f, and num_steps an int >= 0

    Moves d num_steps times; returns the distance
    between the final location and the location
    at the start of the walk.
    """
    start = field.get_location(drunk)
    for step in range(num_steps):
        field.move_drunk(drunk)
    return start.distance_from(field.get_location(drunk))


# Simulating multiple walks
def sim_walks(steps, trials, dClass):
    """Assumes numSteps an int >= 0, numTrials an

    int > 0, dClass a subclass of Drunk
    Simulates numTrials walks of numSteps steps
    each. Returns a list of the final distances
    for each trial
    """
    Homer = dClass()
    distances = []
    origin = Location(0, 0)
    for trial in range(trials):
        field = Field()
        field.add_drunk(Homer, origin)
        distances.append(round(walk(field, Homer, steps), 1))
    return distances


def drunk_test(walk_lengths, trials, dClass):
    """Assumes walkLengths a sequence of ints >= 0
    numTrials an int > 0,
    dClass a subclass of Drunk
    For each number of steps in walkLengths,
    runs simWalks with numTrials walks and
    prints results
    """
    for steps in walk_lengths:
        distances = sim_walks(steps, trials, dClass)
        print(dClass.__name__, "random walk of", steps, "steps")
        print(" Mean =", round(sum(distances) / len(distances), 4))
        print(" Max =", max(distances), "Min =", min(distances))


class OddField(Field):
    def __init__(self, numHoles=1000, xRange=100, yRange=100):
        Field.__init__(self)
        self.wormholes = {}
        for w in range(numHoles):
            x = random.randint(-xRange, xRange)
            y = random.randint(-yRange, yRange)
            newX = random.randint(-xRange, xRange)
            newY = random.randint(-yRange, yRange)
            newLoc = Location(newX, newY)
            self.wormholes[(x, y)] = newLoc

    def moveDrunk(self, drunk):
        Field.moveDrunk(self, drunk)
        x = self.drunks[drunk].getX()
        y = self.drunks[drunk].getY()
        if (x, y) in self.wormholes:
            self.drunks[drunk] = self.wormholes[(x, y)]


if __name__ == "__main__":
    drunk_test((10, 100, 1000, 10000), 100, MasochistDrunk)
    drunk_test((0, 1, 2), 100, MasochistDrunk)

###SUMMARY###
# Point is not the simulations themselves, but how we built them
#
# Started by defining classes
#
# Build functions corresponding to: one trials, multiple trials, resulting report
#
# Made series of incremental changes to stimulation so that we could investigate different questions:
# - Get simple version working first
# - Did a sanity check          
# - Elaborate a step at a time
#
# Showed how to use plots to get insights
