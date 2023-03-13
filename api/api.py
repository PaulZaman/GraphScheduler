from flask import Flask, jsonify
from flask_cors import CORS
from settings import PRJ_DIR
from Graph import Graph
import os

app = Flask(__name__)
CORS(app)

@app.route('/files', methods=['GET'])
def getFiles():
    # iterate through the files in the directory
    files = []
    id=0
    for file in os.listdir(os.path.join(PRJ_DIR, "Graphs")):
        if file.endswith(".txt"):
            files.append({"file":file, "id":id})
            id+=1

    return jsonify({'files': files})

# get all the content from a file
@app.route('/files/<name>', methods=['GET'])
def getFile(name):
    # iterate through the files in the directory
    graphFile = None
    for file in os.listdir(os.path.join(PRJ_DIR, "Graphs")):
        if file.endswith(name):
            graphFile = file

    if not graphFile:
        return jsonify({'error': 'file not found'})
    try:
        g = Graph(graphFile)
        SEND = {
            "fileName":graphFile,
            "constraintTable":g.constraintTable,
            "adjencyMatrix":g.adjencyMatrix,
            "containsCycles":g.scheduler.containsCycles,
            "cycleDetectionSteps":g.scheduler.cycleCheckSteps,
            "edges":g.edgesGraph,
            "lines":g.lines,
            "negativeEdges": g.containsNegativeEdges,
            "ranks": g.scheduler.ranks,
            "criticalPath": g.scheduler.criticalPath,
            "earliestDates": g.scheduler.earliestDates,
            "latestDates": g.scheduler.latestDates,
            "floats": g.scheduler.floats,
        }

        return jsonify(SEND)
    except Exception as e:
        return jsonify({'API Error ': str(e)})

if __name__ == '__main__':
    app.run(debug=True)