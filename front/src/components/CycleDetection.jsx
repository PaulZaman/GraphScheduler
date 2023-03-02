import Table from "./Table";
function CycleDetection({ cycledetectionsteps }) {
  console.log(cycledetectionsteps);
  return (
    <div>
      {Object.keys(cycledetectionsteps).map((step, index) => (
        <div key={index}>
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
