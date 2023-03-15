from settings import *
from Graph import Graph

g = Graph("TestCours.txt")

print(g.scheduler.cycleCheckSteps)
for line in g.scheduler.cycleCheckSteps:
    print(g.scheduler.cycleCheckSteps[line])
