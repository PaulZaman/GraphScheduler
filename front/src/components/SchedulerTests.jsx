import BasicTable from "./SingleEntryTable";
import CycleDetection from "./CycleDetection";
import crossImg from "../assets/cancel.png";
import checkedImg from "../assets/checked.png";

function SchedulerTests({ content, setScheduled }) {
  return (
    <>
      <p className="mt-4 text-lg font-semibold">
        In order to schedule the tasks, we need to make sure the graph:
      </p>
      <ul className="mt-2 ml-8 list-disc">
        <li className="flex">
          Does not contain negative edges{" "}
          {content.negativeEdges ? (
            <img src={crossImg} alt="Not checked" className="h-8 mr-4 pl-2" />
          ) : (
            <img src={checkedImg} alt="checked" className="h-8 mr-4 pl-2" />
          )}
        </li>
        <li className="flex">
          Is acyclic
          {content.containsCycles ? (
            <img src={crossImg} alt="Not checked" className="h-8 mr-4 pl-2" />
          ) : (
            <img src={checkedImg} alt="checked" className="h-8 mr-4 pl-2" />
          )}
        </li>
      </ul>
      <div
        className={`cursor-pointer z-0 rounded p-2 w-40 text-center bg-2 mt-10 ${
          !content.negativeEdges && !content.containsCycles
            ? "scale-animation"
            : "opacity-50"
        } `}
        onClick={() => {
          if (!content.negativeEdges && !content.containsCycles) {
            setScheduled(true);
          }
        }}
      >
        Schedule Graph
      </div>
      <div className="">
        <h1 className="text-3xl font-semibold mt-10 m-auto text-center">
          Negative Edges Check
        </h1>
        <div className="w-1/2 m-auto mt-5">
          <BasicTable
            data={content.edges}
            title="Edge Table"
            columns={[
              { label: "From", property: "from", width: "1/3" },
              { label: "To", property: "to", width: "1/3" },
              { label: "Weight", property: "weight", width: "1/3" },
            ]}
          />
        </div>
        {content.negativeEdges ? (
          <p className="mt-4 text-2xl font-semibold text-center m-auto">
            As we can clearly see, the graph contains negative edges.
          </p>
        ) : (
          <p className="mt-4 text-2xl font-semibold text-center m-auto">
            As we can clearly see, the graph does not contain negative edges.
          </p>
        )}
      </div>
      <div>
        <h1 className="text-3xl font-semibold mt-10 m-auto text-center">
          Cycle check
        </h1>
        <CycleDetection cycledetectionsteps={content.cycleDetectionSteps} />
        {!content.containsCycles ? (
          <p className="mt-4 text-2xl font-semibold text-center m-auto">
            With this algorithm, we have managed to delete all the states,
            Therefore, the graph does not contains any cycles.
          </p>
        ) : (
          <p className="mt-4 text-2xl font-semibold text-center m-auto">
            There are no more steps that we can delete, Therefore, the graph
            contains cycles.
          </p>
        )}
      </div>
    </>
  );
}

export default SchedulerTests;
