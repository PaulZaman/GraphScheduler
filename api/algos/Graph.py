from settings import PRJ_DIR
from Scheduler import Scheduler

class Graph:
    def __init__(self, file):
        self.fileName = file
        self.file = PRJ_DIR + "/graphs/" + file
        self.lines = self.getLines()
        self.constraintTable = self.getConstraintTable()
        self.vertices = self.getVertices()
        self.edges = self.getEdges()
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
        constraintTable.append({"vertice": str(len(constraintTable)), "duration": "0", "constraints": []})   # set last task to N+1

        # add tasks that are not constraints to the last task
        for line in constraintTable:
            found = False
            for line2 in constraintTable:
                if line["vertice"] in line2["constraints"]:
                    found = True
            if not found and line["vertice"] != "0" and line["vertice"] != str(len(constraintTable)-1):
                constraintTable[-1]["constraints"].append(line["vertice"])

        return constraintTable

    def getVertices(self):
        """
        Gets the vertices from the constraint table
        :return: array of vertices
        """
        vertices = []
        for line in self.constraintTable:
            vertices.append(line["vertice"])
        return vertices

    def getAdjencyMatrix(self):
        """
        Gets the adjency table from the edges table
        :return: matrix N*N with N being the number of vertices
        """
        # create a matrix of size len(constraintTable) x len(constraintTable) filling it with '*'
        valueTable = [["*" for x in range(len(self.constraintTable))] for y in range(len(self.constraintTable))]
        for line in self.edges:
            valueTable[int(line["from"])][int(line["to"])] = str(self.getDurationOfVertice(line["from"]))
        return valueTable

    def checkForNegativeEdges(self):
        """
        Checks if the graph has negative edges
        :return: bool
        """
        for line in self.edges:
            if int(line["weight"]) < 0:
                return True
        return False

    def getEdges(self):
        """
        Gets the edges from the constraint table
        :return:  graph as an array of dicts like this {'from': '0', 'to': '1', weight: '1'}
        """
        graph = []

        # add the vertice link to the scheduling graph
        for line in self.constraintTable:
            for constraint in line["constraints"]:
                graph.append({"from":constraint, "to":line["vertice"], "weight":self.getDurationOfVertice(constraint)})

        # order the graph in the order of the from vertice, starting with 0
        graph = sorted(graph, key=lambda k: k["from"])

        return graph

    #### Vertice functions ####

    def getSuccessors(self, vertice, valTable=None):
        """
        Gets the successors of a vertice using the value table
        :param vertice: the vertice
        :return: list of successors
        """
        if valTable is None:
            valTable = self.adjencyMatrix
        successors = []
        for i in range(len(valTable[int(vertice)])):
            if valTable[int(vertice)][i] != "*":
                successors.append(i)

        return successors

    def getPredecessors(self, vertice, valTable=None):
        """
        Gets the predecessors of a vertice
        :param vertice: the vertice
        :return: list of predecessors
        """
        if valTable is None:
            valTable = self.adjencyMatrix
        predecessors = []
        for i in range(len(valTable)):
            if valTable[i][int(vertice)] != "*":
                predecessors.append(i)
        return predecessors

    def getDurationOfVertice(self, vertex):
        if type(vertex) == int:
            vertex = str(vertex)
        for line in self.constraintTable:
            if (line["vertice"] == vertex):
                return line["duration"]
        return False

    def getWeight(self, start, end):
        """
        Gets the weight of an edge
        :param start: the start vertice
        :param end: the end vertice
        :return: the weight of the edge as an integer, or None if no edge exists,
        """
        for edge in self.edges:
            if edge["from"] == str(start) and edge["to"] == str(end):
                return int(edge["weight"])
        return None

    #### Path functions ####

    def getPath(self, start, end, path=None):
        """
        Recursive function to find a path from start to end in the graph
        :param start: the start vertex
        :param end: the end vertex
        :param path: the path from start to end
        :return: the path from start to end
        """
        if path is None:
            path = []  # initialize path on first call

        path.append(start)  # add current vertex to path

        if start == end:
            return path  # return path if end vertex is found

        if self.getSuccessors(start) == []:
            path.pop()
            return None  # return None if no path exists

        for successor in self.getSuccessors(start):
            subpath = self.getPath(successor, end, path)
            if subpath is not None:
                return subpath  # return subpath if end vertex is found

        path.pop()  # remove current vertex from path if no path found
        return None

    def getAllPaths(self, start, end, path=None, paths=None):
        """
        Recursive function to find all paths from start to end in the graph
        :param start: the start vertex
        :param end: the end vertex
        :param path: the path from start to end
        :param paths: the list of paths from start to end
        :return: the list of paths from start to end
        """
        if path is None:
            path = []  # initialize path on first call
        if paths is None:
            paths = []  # initialize paths on first call

        path.append(start)  # add current vertex to path

        if start == end:
            paths.append(path.copy())  # copy current path and add to paths list
        else:
            if self.getSuccessors(start) == []:
                path.pop()
                return None  # return None if no path exists
            else:
                for successor in self.getSuccessors(start):
                    self.getAllPaths(successor, end, path, paths)

        path.pop()  # remove current vertex from path
        return paths

    def getDurationOfPath(self, path):
        """
        Function to find the duration of a path
        :param path: the path in array form
        :return: the duration of the path as int
        """
        duration = 0
        for i in range(len(path)):
            if i != len(path) - 1:
                duration += int(self.getDurationOfVertice(path[i]))
        return duration

    def getLongestPath(self, start, end):
        """
        Function to find the maximum duration path in the graph
        :param start: the start vertex
        :param end: the end vertex
        :return: the maximum duration path as list
        """
        maxDurationIndex = 0
        paths = self.getAllPaths(start, end)
        if (paths == None):
            return None
        for path in paths:
            duration = self.getDurationOfPath(path)
            if duration > self.getDurationOfPath(paths[maxDurationIndex]):
                maxDurationIndex = paths.index(path)
        return paths[maxDurationIndex]



