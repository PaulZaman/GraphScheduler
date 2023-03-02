import copy


class Scheduler:
    def __init__(self, graph):
        self.graph = graph
        self.constraintTable = graph.constraintTable
        self.adjencyMatrix = graph.adjencyMatrix
        self.cycleCheckSteps, self.containsCycles = self.detectCycle()

    def stateAdmitsSucessors(self, valTable, stateN):
        """
        Checks if the state admits sucessors
        :param valTable: value table to check
        :param stateN: state index to check
        :return: bool
        """
        for el in valTable[stateN]:
            if el != "*":
                return True
        return False

    def stateAdmitsPredecessors(self, valTable, stateN):
        """
        Checks if the state admits predecessors
        :param valTable: value table to check
        :param stateN: state index to check
        :return: bool
        """
        for line in valTable:
            if line[stateN] != "*":
                return True
        return False

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

        valTable = self.adjencyMatrix.copy()
        Steps = {}
        Steps[0] = {"valueTable":copy.deepcopy(valTable), "deletedSteps": [], "vertices":[i for i in range(len(self.adjencyMatrix))]}   # dict of steps

        for j in range(1, len(self.adjencyMatrix) + 1):
            # Find states that hav no predecessors or no sucessors
            # add them to the states to delete array
            statesIndexToDelete = []
            for i in range(len(valTable)):
                if not self.stateAdmitsPredecessors(valTable, i):
                    statesIndexToDelete.append(i)
                if not self.stateAdmitsSucessors(valTable, i):
                    statesIndexToDelete.append(i)

            # order the states to delete in reverse order
            statesIndexToDelete = sorted(statesIndexToDelete, reverse=True)

            # check if the value table is empty (before deleting the states cause you can't delete from empty array)
            if (len(valTable) <= 1):
                return Steps, False

            #eliminate duplicates
            statesIndexToDelete = list(dict.fromkeys(statesIndexToDelete))

            # delete the states from the value table + delete from the array of vertices
            vertices = copy.deepcopy(Steps[j-1]["vertices"])

            deletedStates = []
            for state in statesIndexToDelete:
                valTable = self.removeStateFromMatrix(valTable, state)
                deletedStates.append(vertices.pop(state))

            # DISPLAY
            '''print("Step " + str(j) + ":")
            print("Value Table: ")
            for line in valTable:
                print(line)
            print("Deleted States: " + str(deletedStates))
            print("Vertices: " + str(vertices))
            print("")'''

            # return if there are no more states to delete
            if len(statesIndexToDelete) == 0:
                return Steps, True

            #add this step to the steps dict
            Steps[j] = {"valueTable": copy.deepcopy(valTable), "deletedSteps": deletedStates, "vertices":vertices}

        return Steps, True


