import Graph from "./Graph";
import ScheduleTable from "../Tables/ScheduleTable";
import BasicTable from "../Tables/SingleEntryTable";
import { useEffect } from "react";

function Scheduled({ setScheduled, content }) {
  let canBeScheduled = !content.containsCycles && !content.negativeEdges;
  // go back to tests if content changes
  useEffect(() => {
    canBeScheduled = !content.containsCycles && !content.negativeEdges;
    if (!canBeScheduled) setScheduled(false);
  }, [content]);

  console.log(content);
  return (
    <>
      {!canBeScheduled ? (
        <div>Can't Be Scheduled</div>
      ) : (
        <div className="justify-center mt-16 w-full">
          <div
            className="rounded p-2 w-40 text-center bg-2 scale-animation cursor-pointer m-auto"
            onClick={() => setScheduled(false)}
          >
            Back to Tests
          </div>
          <div className=" w-10/12 p-10 m-auto mt-10 border-white border-2 items-center">
            <div className="text-bold text-3xl text-center mb-10">
              Ranks of the Vertices
            </div>
            <BasicTable
              data={content.ranks}
              title=""
              columns={[
                { label: "Vertice", property: "vertice", width: "auto" },
                { label: "Rank", property: "rank", width: "auto" },
              ]}
            />

            {/* GRAPH SCHEME */}
            <Graph
              edges={content.edges}
              startnode={content.constraintTable[0].vertice}
              endnode={
                content.constraintTable[content.constraintTable.length - 1]
                  .vertice
              }
              criticalPath={content.criticalPath}
            />
          </div>

          <div className=" w-10/12 p-10 m-auto mt-10 border-white border-2 items-center">
            <div className="text-bold text-3xl text-center w-full">
              Calendar{" "}
            </div>
            <ScheduleTable
              schedule={content.earliestDates}
              title="Earliest Date Calendar"
            />
            <ScheduleTable
              schedule={content.latestDates}
              title="Latest Date Calendar"
            />
            <ScheduleTable schedule={content.floats} title="Floats" />
          </div>

          <div className=" w-10/12 p-10 m-auto mt-10 border-white border-2 items-center">
            <div className="text-bold text-3xl text-center w-full">
              Critical Path
            </div>
            <div className="text-bold text-3xl text-center w-full mt-10">
              {content.criticalPath.join(" -> ")}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Scheduled;
