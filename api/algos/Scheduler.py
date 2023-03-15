import copy

class Scheduler:
    def __init__(self, graph):
        self.graph = graph
        self.constraintTable = graph.constraintTable
        self.adjencyMatrix = graph.adjencyMatrix
        self.cycleCheckSteps, self.containsCycles = self.detectCycle()
        self.containsNegativeEdges = graph.containsNegativeEdges
        self.canBeScheduled = False
        self.ranks = None
        self.earliestDates = None
        self.latestDates = None
        self.floats = None
        self.criticalPath = None
        self.canBeScheduled = not (self.containsCycles or self.containsNegativeEdges)
        if self.canBeScheduled:
            self.ranks = self.getRanks()
            self.earliestDates, self.latestDates, self.floats, self.criticalPath = self.getSchedule()


    def removeStateFromMatrix(self, m, stateN):
        """
        Removes a state from the value table (line + column)
        :param valTable: value table to remove from
        :param stateN: state index to remove
        :return: None
        """
        m1 = copy.deepcopy(m)
        m1.pop(stateN)
        for line in m1:
            line.pop(stateN)
        return m1

    def detectCycle(self):
        """
        Detects if the Graph has a cycle or not
        :return: bool
        """
        # copy value table
        valTable = self.adjencyMatrix.copy()

        # initialize the steps dictionary, in order to keep track of the steps
        Steps = {}
        Steps[0] = {
            "valueTable":copy.deepcopy(valTable),
            "deletedSteps": [],
            "vertices": [i for i in range(len(self.adjencyMatrix))]
        }

        # Loop until the value table is empty, or until there are no more states to delete
        # (no more states with no predecessors or no sucessors)
        for j in range(1, len(self.adjencyMatrix) + 1):
            # If the value table is empty return false (no cycle)
            if (len(valTable) <= 1):
                return Steps, False

            # find the index of the states to delete
            statesIndexToDelete = self.getStatesToDelete(valTable)

            # initialize the "vertices" list
            vertices = copy.deepcopy(Steps[j-1]["vertices"])

            # delete the states from the value table
            deletedStates = []
            for stateI in statesIndexToDelete:
                valTable = self.removeStateFromMatrix(valTable, stateI)
                deletedStates.append(vertices.pop(stateI))

            # Return if there are no more states to delete
            if len(statesIndexToDelete) == 0:
                return Steps, True

            # Add this step to the steps dict
            Steps[j] = {"valueTable": copy.deepcopy(valTable), "deletedSteps": deletedStates, "vertices": vertices}

            # DISPLAY
            '''print("Step " + str(j) + ":")
            print("Value Table: ")
            for line in valTable:
                print(line)
            print("Deleted States: " + str(deletedStates))
            print("Vertices: " + str(vertices))
            print("")'''

        # return if there are no more states to delete
        return Steps, True

    def getStatesToDelete(self, valTable):
        """
        Gets the states that can be deleted from the value table
        :param valTable: value table to check
        :return: list of index of states to delete
        """
        statesIndexToDelete = []
        for i in range(len(valTable)):
            # if the state has no predecessors
            if len(self.graph.getPredecessors(i, valTable=valTable))==0:
                statesIndexToDelete.append(i)
            # if the state has no sucessors
            elif len(self.graph.getSuccessors(i, valTable=valTable))==0:
                statesIndexToDelete.append(i)

        # order the states to delete in reverse order
        statesIndexToDelete = sorted(statesIndexToDelete, reverse=True)

        # eliminate duplicates
        statesIndexToDelete = list(dict.fromkeys(statesIndexToDelete))

        return statesIndexToDelete

    def getRanks(self):
        if not self.canBeScheduled:
            return None
        # initialize the ranks list
        ranks = [0 for i in range(len(self.adjencyMatrix))]

        position = [
            (0, 0), # (statenumber, timeEnteredAtThisState)
        ]
        # loop until all states have a rank
        while len(position) != 0:
            # get the state number and the time entered at this state
            stateNumber, timeEnteredAtThisState = position.pop(0)
            # if the state has no predecessors, then it has a rank of 0
            if len(self.graph.getPredecessors(stateNumber)) == 0:
                ranks[stateNumber] = 0
            # if the state has predecessors
            else:
                # get the maximum rank of the predecessors
                maxRank = max([ranks[pred] for pred in self.graph.getPredecessors(stateNumber)])
                # if the maximum rank is equal to the time entered at this state, then the state has a rank of maxRank + 1
                if maxRank == timeEnteredAtThisState:
                    ranks[stateNumber] = maxRank + 1
                # else, the state has a rank of maxRank
                else:
                    ranks[stateNumber] = maxRank
            # add the successors of the state to the position list
            for succ in self.graph.getSuccessors(stateNumber):
                position.append((succ, ranks[stateNumber]))

        ret = []
        for i in range(len(ranks)):
            ret.append({"vertice": i, "rank": ranks[i]})
        return ret

    def getSchedule(self):
        if not self.canBeScheduled:
            return None
        column1 = ["Rank", "Vertice", "Duration", "Predecessor", "Dates per predecessor", "Successors",  "Dates per successor", "Earliest Date", "Latest Date", "Total Float"]
        ranks = []
        vertices = []
        durations = []
        predecessors = []
        successors = []
        datesPerPredecessor = []
        datesPerSuccessor = []
        earliestDates = []
        latestDates = []
        totalFloats = []

        # fill the ranks, vertices, durations, predecessors and successors lists
        ranksDict = self.getRanks()
        ranksDict = sorted(ranksDict, key=lambda k: k['rank'])
        for rank in ranksDict:
            ranks.append(rank["rank"])
            vertices.append(rank["vertice"])
            durations.append(int(self.graph.getDurationOfVertice(rank["vertice"])))
            predecessors.append(self.graph.getPredecessors(rank["vertice"]))
            successors.append(self.graph.getSuccessors(rank["vertice"]))
            datesPerPredecessor.append([])
            datesPerSuccessor.append([])

        # fill the datesPerPredecessor list
        datesPerPredecessor[0] = [0]
        for i in range(len(vertices)):
            for pred in predecessors[i]:
                d = int(self.graph.getDurationOfVertice(pred)) # find duration of predecessor
                if len(datesPerPredecessor[vertices.index(pred)]) == 0:
                    date  = 0 # if the predecessor has no dates, then the date is 0
                else:
                    date = max(datesPerPredecessor[vertices.index(pred)]) + d # find the Date of the predecessor
                datesPerPredecessor[i].append(date)  # add the date to the datesPerPredecessor list

        # fill the earliestDates list
        for i in range(len(vertices)):
            earliestDates.append(max(datesPerPredecessor[i]))


        # fill the datesPerSuccessor list
        datesPerSuccessor[len(vertices)-1] = [min(datesPerPredecessor[len(vertices)-1])]
        for i in range(len(vertices)-1, -1, -1):
            for succ in successors[i]:
                date = min(datesPerSuccessor[vertices.index(succ)]) - durations[i]
                datesPerSuccessor[i].append(date)

        # fill the latestDates list
        for i in range(len(vertices)):
            latestDates.append(min(datesPerSuccessor[i]))

        # fill the totalFloats list
        for i in range(len(vertices)):
            totalFloats.append(latestDates[i] - earliestDates[i])

        latestDatesDict = {
            "headers": ["Ranks", "Vertices", "Durations", "Successors", "Dates of Successors", "Latest Dates"],
            "Ranks" : ranks,
            "Vertices" : vertices,
            "Durations" : durations,
            "Successors" : successors,
            "Dates of Successors" : datesPerSuccessor,
            "Latest Dates" : latestDates
        }

        earliestDatesDict = {
            "headers": ["Ranks", "Vertices", "Durations", "Predecessors", "Dates of Predecessors", "Earliest Dates"],
            "Ranks" : ranks,
            "Vertices" : vertices,
            "Durations" : durations,
            "Predecessors" : predecessors,
            "Dates of Predecessors" : datesPerPredecessor,
            "Earliest Dates" : earliestDates
        }

        floats = {
            "headers": ["Ranks", "Vertices", "Durations", "Earliest Dates", "Latest Dates", "Total Floats"],
            "Ranks" : ranks,
            "Vertices" : vertices,
            "Durations" : durations,
            "Earliest Dates" : earliestDates,
            "Latest Dates" : latestDates,
            "Total Floats" : totalFloats
        }

        # add "-" to the succesors and predecessors lists if they are empty
        for i in range(len(vertices)):
            if len(predecessors[i]) == 0:
                predecessors[i] = ["-"]
            if len(successors[i]) == 0:
                successors[i] = ["-"]

        criticalPath = []
        for i in range(len(vertices)):
            if totalFloats[i] == 0:
                criticalPath.append(vertices[i])

        """from prettytable import PrettyTable
        # Create a table
        table = PrettyTable()
        # insert titles
        ranks.insert(0, column1[0])
        vertices.insert(0, column1[1])
        durations.insert(0, column1[2])
        predecessors.insert(0, column1[3])
        datesPerPredecessor.insert(0, column1[4])
        successors.insert(0, column1[5])
        datesPerSuccessor.insert(0, column1[6])
        earliestDates.insert(0, column1[7])
        latestDates.insert(0, column1[8])
        totalFloats.insert(0, column1[9])

        # Add columns to the table
        table.add_row(ranks)
        table.add_row(vertices)
        table.add_row(durations)
        table.add_row(predecessors)
        table.add_row(datesPerPredecessor)
        table.add_row(earliestDates)
        table.add_row(successors)
        table.add_row(datesPerSuccessor)
        table.add_row(latestDates)
        table.add_row(totalFloats)

        # Set the header to an empty string
        table.header = False
        # Print the table
        print("Schedule:")
        print(table)
        
        print("Critical Path:")
        print(criticalPath)"""

        return earliestDatesDict, latestDatesDict, floats, criticalPath

    def displayArrayOfDicts(self, array):
        import prettytable as pt
        table = pt.PrettyTable()
        headers = array[0].keys()
        table.field_names = headers
        for i in range(len(array)):
            row = []
            for header in headers:
                row.append(array[i][header])
            table.add_row(row)

        print(table)

    def findPath(self, start, end, path=None):
        if path is None:
            path = []  # initialize path on first call

        path.append(start)  # add current vertex to path

        if start == end:
            return path  # return path if end vertex is found

        if self.graph.getSuccessors(start) == []:
            path.pop()
            return None  # return None if no path exists

        for successor in self.graph.getSuccessors(start):

            subpath = self.pathExists(successor, end, path)
            if subpath is not None:
                return subpath  # return subpath if end vertex is found

        path.pop()  # remove current vertex from path if no path found
        return None

    def findAllPaths(self, start, end, path=None, paths=None):
        if path is None:
            path = []  # initialize path on first call
        if paths is None:
            paths = []  # initialize paths on first call

        path.append(start)  # add current vertex to path

        if start == end:
            paths.append(path.copy())  # copy current path and add to paths list
        else:
            if self.graph.getSuccessors(start) == []:
                path.pop()
                return None  # return None if no path exists
            else:
                for successor in self.graph.getSuccessors(start):
                    self.findAllPaths(successor, end, path, paths)

        path.pop()  # remove current vertex from path
        return paths

    def findDurationOfPath(self, path):
        duration = 0
        for i in range(len(path)):
            if i != len(path) - 1:
                duration += int(self.graph.getDurationOfVertice(path[i]))
        return duration

    def findMinimumDurationPath(self, start, end):
        minDurationIndex = 0
        paths = self.findAllPaths(start, end)
        if (paths == None):
            return None
        for path in paths:
            duration = self.findDurationOfPath(path)
            if duration < self.findDurationOfPath(paths[minDurationIndex]):
                minDurationIndex = paths.index(path)

        return paths[minDurationIndex]

    def deleteLastEdgeInPath(self, path, edges):
        # remove last edge in path p
        v1 = path[len(path) - 2]
        v2 = path[len(path) - 1]
        for edge in edges:
            if edge["from"] == v1 and edge["to"] == v2:
                edges.remove(edge)
                break

    def optimize(self):
        edgesGraph = copy.deepcopy(self.graph.edgesGraph)
        finished = False
        while not finished:
            for v1 in range(len(self.graph.constraintTable)):
                finished = True
                for v2 in range(len(self.graph.constraintTable)):
                    paths = self.findAllPaths(str(v1), str(v2))
                    if paths and len(paths)>1:
                        p = self.findMinimumDurationPath(str(v1), str(v2))
                        # remove last edge in path p
                        self.deleteLastEdgeInPath(p, edgesGraph)
                        finished = False

        return edgesGraph