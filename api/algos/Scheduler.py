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
            #self.bellman('0')

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

    def detectCycle(self, onlyPredecessors=False):
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
            if (len(valTable) < 1):
                return Steps, False

            # find the index of the states to delete
            statesIndexToDelete = self.getStatesToDelete(valTable, onlyPredecessors=onlyPredecessors)

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

    def getStatesToDelete(self, valTable, onlyPredecessors=False):
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
            if not onlyPredecessors:
                # if the state has no sucessors
                if len(self.graph.getSuccessors(i, valTable=valTable))==0:
                    statesIndexToDelete.append(i)

        # order the states to delete in reverse order
        statesIndexToDelete = sorted(statesIndexToDelete, reverse=True)

        # eliminate duplicates
        statesIndexToDelete = list(dict.fromkeys(statesIndexToDelete))

        return statesIndexToDelete

    def getRanks(self):
        cycleSteps = self.detectCycle(onlyPredecessors=True)[0]
        ranks = []
        for i in range(len(cycleSteps)):
            for state in cycleSteps[i]["deletedSteps"]:
                ranks.append({"vertice": state, "rank": i-1})
        return ranks

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
        freeFloats = []

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
        datesPerSuccessor[len(vertices)-1] = [max(datesPerPredecessor[len(vertices)-1])]
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
        
        # fill the freeFloats list
        for i in range(len(vertices)):
            # if the vertice has no successors, then the free float is 0
            if len(successors[i]) == 0:
                freeFloats.append(0)
            else:
                ## get successors
                succs = successors[i]
                ## get the earliest date of the successors
                earliestDateOfSuccs = min([earliestDates[vertices.index(succ)] for succ in succs])
                freeFloats.append(earliestDateOfSuccs - earliestDates[i])



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
            "headers": ["Ranks", "Vertices", "Durations", "Earliest Dates", "Latest Dates", "Total Floats", "Free Floats"],
            "Ranks" : ranks,
            "Vertices" : vertices,
            "Durations" : durations,
            "Earliest Dates" : earliestDates,
            "Latest Dates" : latestDates,
            "Total Floats" : totalFloats,
            "Free Floats" : freeFloats
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

    def bellman(self, verticeA):
        """
        This function implements the Bellman-Ford algorithm to find the shortest path from a vertice to all other vertices.
        :param verticeA: the vertice from which the shortest path is calculated
        :return: a matrix with the shortest path from verticeA to all other vertices
        """
        bellman_columns = ['k'] + [str(vertice) for vertice in self.graph.getVertices()]

        # first iteration
        bellman = []
        initial_row = [0]
        for vertice in self.graph.getVertices():
            if vertice == verticeA:
                initial_row.append(0)
            else:
                initial_row.append(float('inf'))
        bellman.append(initial_row)
        verticestoCheck = [verticeA]


        cpt: int = 0
        while  not(len(verticestoCheck) == 0):
            # new iteration, augment k by 1
            bellman.append(copy.deepcopy(bellman[cpt]))
            cpt += 1
            bellman[cpt][0] = cpt
            for v in verticestoCheck:
                successors = self.graph.getSuccessors(v)
                for successor in successors:
                    index = bellman_columns.index(str(successor))
                    weight = self.graph.getWeight(v, successor)
                    bellman[cpt][index] = min(bellman[cpt][index], bellman[cpt-1][bellman_columns.index(str(v))] + weight)

            # update the verticestoCheck list
            verticestoCheck = []
            for i in range(1, len(bellman[cpt])):
                if bellman[cpt][i] != bellman[cpt-1][i]:
                    verticestoCheck.append(bellman_columns[i])


        from prettytable import PrettyTable

        table = PrettyTable()
        table.field_names = bellman_columns
        for line in bellman:
            table.add_row(line)
        print(table)








