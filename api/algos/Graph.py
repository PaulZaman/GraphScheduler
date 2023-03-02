from settings import PRJ_DIR
from Scheduler import Scheduler

def displayIterableInTerminal(iterable):
    for item in iterable:
        print(item)


class Graph:
    def __init__(self, file):
        self.file = PRJ_DIR + "/graphs/" + file
        self.lines = self.getLines()
        self.constraintTable = self.getConstraintTable()
        self.edgesGraph = self.getEdges()
        self.adjencyMatrix = self.getAdjencyMatrix()
        self.containsNegativeEdges = self.checkForNegativeEdges()

        # create scheduler
        self.scheduler = Scheduler(self)

    def getLines(self):
        return [line.rstrip('\n') for line in open(self.file)]

    def getConstraintTable(self):
        """
        Function that gets the constraint table from the lines of the file
        Creates 1rst vertice "0", and last vertice (N+1)
        :return: arr of dicts like this {'vertice': '0', 'duration': '0', 'constraints': []}
        """
        # create a list with the constraint table
        constraintTable = [{"vertice": "0", "duration": "0", "constraints": []}]   # set first task to 0

        # split each line in the file
        lines = [line.split(" ") for line in self.lines]
        # for each line in the file, add the task, duration, and constraints to the constraint table
        for line in lines:
            constraintTable.append({"vertice": line[0], "duration": line[1], "constraints": line[2:]})
            # add first task to constraints if no constraints
            if not constraintTable[-1]["constraints"]:
                constraintTable[-1]["constraints"] = ["0"]

        # add last task to the constraint table
        constraintTable.append({"vertice": str(len(constraintTable)), "duration": "0", "constraints": []})   # set last task to omega

        # add tasks that are not constraints to the last task
        for line in constraintTable:
            found = False
            for line2 in constraintTable:
                if line["vertice"] in line2["constraints"]:
                    found = True
            if not found and line["vertice"] != "0" and line["vertice"] != str(len(constraintTable)-1):
                constraintTable[-1]["constraints"].append(line["vertice"])

        return constraintTable

    def getAdjencyMatrix(self):
        """
        Gets the value table from the constraint table
        :return: matrix under the form given in the subject corresponding to the value table
        """
        # create a matrix of size len(constraintTable) x len(constraintTable) filling it with '*'
        valueTable = [["*" for x in range(len(self.constraintTable))] for y in range(len(self.constraintTable))]
        for line in self.edgesGraph:
            valueTable[int(line["from"])][int(line["to"])] = str(1)
        return valueTable

    def checkForNegativeEdges(self):
        """
        Checks if the graph has negative edges
        :return: bool
        """
        for line in self.edgesGraph:
            if int(line["weight"]) < 0:
                return True
        return False

    def findDurationOfVertice(self, vertice):
        for line in self.constraintTable:
            if (line["vertice"] == vertice):
                return line["duration"]
        return False

    def getEdges(self):
        """
        Gets the  Graph from the constraint table
        :return:  graph as an array of dicts like this {'from': '0', 'to': '1', weight: '1'}
        """
        graph = []

        # add the vertice link to the scheduling graph
        for line in self.constraintTable:
            for constraint in line["constraints"]:
                graph.append({"from":constraint, "to":line["vertice"], "weight":self.findDurationOfVertice(constraint)})

        # order the graph in the order of the from vertice, starting with 0
        graph = sorted(graph, key=lambda k: k["from"])

        return graph

