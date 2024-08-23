import operator
import math
import random

import numpy

from functools import partial

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from typing import List

"""high mutation rate with elitism would prob lower error rate"""
"""most of this is taken directly from deap's example"""



def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

def protectedPow(base, big):
    print(base)
    print(big)
    if big < 0 or not isinstance(big, int):
        return 1
    else:
        return math.pow(base, big)


def do_gp(sequence: List[int]):
    pset = gp.PrimitiveSet("MAIN", 1)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(protectedDiv, 2)
    pset.addPrimitive(operator.neg, 1)
    #pset.addPrimitive(protectedPow, 2)
    pset.addEphemeralConstant("randint", partial(random.randint, -5, 5))
    pset.renameArguments(ARG0='x')

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)

    def pairwiseEval(points, individual):
        """
        this one is different
        points are the values in the recurrent sequence
        we want to minimize the errors moving forward
        mean squared error
        TODO: figure out how to do both individual (one pair of values at a time), and eval across a lot of things
        IMPORTANT: maybe change the fitness values as we move forwards, like iniitially focus on the pairwise fitness
                    as a 'hint',but move on to fitness after the recursion is applied many times to 'fine-tune' the model

        how would I do this for recurrences with more than one term back - fibonacci?
        """
        # Transform the tree expression in a callable function
        func = toolbox.compile(expr=individual)
        error = 0
        print(individual)
        for i in range(len(points)-1):
            #print(func(points[i]))
            ind = func(points[i])-points[i+1]
            error = error + ind**2

        return error/(len(points)-1), #-1 because each pair of consecutive values is a sample

    toolbox.register("evaluate", pairwiseEval, sequence)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

    #seed 1 just happens to be the corerct soltion
    random.seed(139)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 10, stats=mstats,
                                   halloffame=hof, verbose=True)
    # print log
    return pop, log, hof
