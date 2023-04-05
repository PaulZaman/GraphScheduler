from settings import *
from Graph import Graph
## In this part of the project, we test run all the files in the Graphs folder

# iterate through the files in the directory
n_Files = 0
n_Failed = 0
for file in os.listdir(os.path.join(PRJ_DIR, "Graphs")):
    if file.endswith(".txt"):
        n_Files += 1
        try:
            g = Graph(file)
            print("File: ", file, " test completed")
        except Exception as e:
            print("File: ", file, " test failed")
            print(e)
            n_Failed += 1

# print the results
print("")
print("Number of files tested: ", n_Files)
print("Number of files failed: ", n_Failed)
print("Number of files passed: ", n_Files - n_Failed)
print("Percentage of files passed: ", (n_Files - n_Failed) / n_Files * 100, "%")



