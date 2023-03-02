# This file was for the course, and is not part of the project

def stateAdmitsSucessors(valTable, stateN):
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


def stateAdmitsPredecessors(valTable, stateN):
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


def removeStateFromValueTable(valTable, stateN):
    """
    Removes a state from the value table (line + column)
    :param valTable: value table to remove from
    :param stateN: state index to remove
    :return: None
    """
    valTable.pop(stateN)
    for line in valTable:
        line.pop(stateN)
    return valTable


def copyMatrix(matrix):
    """
    Copies a matrix
    :param matrix: matrix to copy
    :return: the copied matrix
    """
    return [line.copy() for line in matrix.copy()]


def detectCycle(AdjencyMatrix):
    """
    Detects if the Graph has a cycle or not
    :return: bool
    """
    valTable = AdjencyMatrix.copy()
    Steps = {}
    Steps[0] = {"valueTable": copyMatrix(valTable), "deletedSteps": []}  # dict of steps
    for j in range(1, len(AdjencyMatrix) + 1):
        # Find states that hav no predecessors or no sucessors
        # add them to the states to delete array
        statesToDelete = []
        for i in range(len(valTable)):
            if not stateAdmitsPredecessors(valTable, i):
                statesToDelete.append(i)
            if not stateAdmitsSucessors(valTable, i):
                statesToDelete.append(i)

        # order the states to delete in reverse order
        statesToDelete = sorted(statesToDelete, reverse=True)

        # check if the value table is empty (before deleting the states cause you can't delete from empty array)
        if not (len(valTable) > 1):
            print("No cycle detected")
            return Steps, False

        # delete the states from the value table
        for state in statesToDelete:
            valTable = removeStateFromValueTable(valTable, state)

        # add this step to the steps dict
        Steps[j] = {"valueTable": copyMatrix(valTable), "deletedSteps": statesToDelete}


def disp(valTable):
    for line in valTable:
        print(line)


adjencyMatrix = [
    # 0    1    2    3    4    5    6
    ['*', '0', '0', '*', '*', '*', '*'],    # 0
    ['*', '*', '*', '1', '1', '*', '*'],    # 1
    ['*', '*', '*', '*', '2', '2', '*'],    # 2
    ['*', '*', '*', '*', '*', '*', '3'],    # 3
    ['*', '*', '*', '*', '*', '4', '*'],    # 4
    ['*', '*', '*', '*', '*', '*', '5'],    # 5
    ['*', '*', '*', '*', '*', '*', '*']     # 6
]

steps, res = detectCycle(adjencyMatrix);
for i in range(len(steps)):
    print("Step n°" + str(i))
    print("Deleted states: " + str(steps[i]["deletedSteps"]))
    print("Value table: ")
    for line in steps[i]["valueTable"]:
        print(line)
    print("")