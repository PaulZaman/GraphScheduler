# import graph class
from settings import *
from Graph import Graph
import os
from veryprettytable import VeryPrettyTable
## In this part of the project, we test run all the files in the Graphs folder


class ExecutionTraces:
    def __init__(self, graph):
        self.graph = graph
        self.executionTraces = []
        with open(os.path.join(execPath, self.graph.fileName), "w") as file:
            file.write("Execution Trace for " + self.graph.fileName)
            file.write("\n\n\n")
            self.fileContent(file)
            self.constraintTable(file)
            self.adjacenyMatrix(file)
            self.cycleDetection(file)
            if self.graph.scheduler.canBeScheduled:
                self.negativeEdges(file)
                self.ranks(file)
                self.calendars(file)
                self.criticalPath(file)
            else:
                file.write("\n\nCAN NOT BE SCHEDULED")
    def fileContent(self, file):
        file.write("File Content:")
        file.write("\n\n")
        for line in self.graph.lines:
            file.write(line + "\n")
        file.write("\n\n\n")

    def constraintTable(self, file):
        file.write("Constraint Table:")
        file.write("\n\n")
        self.verticalTableFromArrayOfDict(self.graph.constraintTable, file)

    def adjacenyMatrix(self, file):
        file.write("Adjaceny Matrix:")
        file.write("\n\n")
        self.doubleEntryTable(self.graph.adjencyMatrix, file, self.graph.vertices)

    def cycleDetection(self, file):
        file.write("\n\nCycle Detection:")
        file.write("\n\n")
        file.write("Contains Cycles: " + str(self.graph.scheduler.containsCycles))
        file.write("\n\n")
        file.write("Steps:")
        file.write("\n\n")
        for dicti in self.graph.scheduler.cycleCheckSteps:
            step = self.graph.scheduler.cycleCheckSteps[dicti]
            file.write("Step " + str(dicti) + ":")
            file.write("\n")
            self.doubleEntryTable(step["valueTable"], file, step["vertices"])
            file.write("Deleted Edges: " + str(step["deletedSteps"]) + "\n")

    def ranks(self, file):
        file.write("\n\nRanks:")
        file.write("\n\n")
        self.verticalTableFromArrayOfDict(self.graph.scheduler.ranks, file)

    def criticalPath(self, file):
        file.write("\n\nCritical Path: " + str(self.graph.scheduler.criticalPath))
        file.write("\n\n")

    def calendars(self, file):
        file.write("Earliest Dates:")
        file.write("\n\n")
        self.display_table(file, self.graph.scheduler.earliestDates)
        file.write("\n\n")
        file.write("Latest Dates:")
        file.write("\n\n")
        self.display_table(file, self.graph.scheduler.latestDates)
        file.write("\n\n")
        file.write("Floats:")
        file.write("\n\n")
        self.display_table(file, self.graph.scheduler.floats)

    def negativeEdges(self, file):
        file.write("\n\n")
        file.write("Contains Negative Edges: " + str(self.graph.scheduler.containsNegativeEdges))
        file.write("\n\n")

    ## general table functions
    def verticalTableFromArrayOfDict(self, array, file):
        table = VeryPrettyTable()
        table.field_names = list(array[0].keys())
        for line in array:
            table.add_row(list(line.values()))
        file.write(str(table))
        file.write("\n\n\n")

    def doubleEntryTable(self, array, file, field_names):
        table = VeryPrettyTable()

        table.field_names = [""] + field_names
        for i in range(len(array)):
            table.add_row([field_names[i]] + array[i])
        file.write(str(table))
        file.write("\n")

    def display_table(self, file, data):
        table = VeryPrettyTable()
        headers = data['headers']
        for header in headers:
            table.field_names = headers
        rows = len(data[headers[0]])
        for i in range(rows):
            row = []
            for header in headers:
                row.append(data[header][i])
            table.add_row(row)
        file.write(str(table))

# get directory of execution traces
execPath = os.path.join(PRJ_DIR, "ExecutionTraces")

# get all files in the directory
for file in os.listdir(os.path.join(PRJ_DIR, "Graphs")):
    try:
        # if the file is a text file
        if file.endswith(".txt"):
            # create graph object
            g = Graph(file)
            # create execution trace object
            ExecutionTraces(g)
    except:
        print("Error in " + file)




