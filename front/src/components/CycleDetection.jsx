import Table from "./Table";
function CycleDetection({ cycledetectionsteps }) {
  return (
    <div className="flex justify-center flex-wrap p-1">
      {Object.keys(cycledetectionsteps).map((step, index) => (
        <div key={index} className="p-3">
          <Table
            dataMatrix={cycledetectionsteps[step].valueTable}
            title={
              "Step n°" +
              step +
              " : deletion of states " +
              cycledetectionsteps[step].deletedSteps
            }
            topRow={cycledetectionsteps[step].vertices}
            leftCol={cycledetectionsteps[step].vertices}
          />
        </div>
      ))}
    </div>
  );
}

export default CycleDetection;
