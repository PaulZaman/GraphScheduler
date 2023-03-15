import Table from "../Tables/DoubleEntryTable";
import TextComponent from "./TextComponent";
import BasicTable from "../Tables/SingleEntryTable";
import Graph from "./Graph";

function Content({ content }) {
  return (
    <>
      <div className="bg-OxforfBlue">
        {/* TEXT CONTENT OF FILE */}
        <div className="">
          <div className="mx-auto flex ml-32 mr-32">
            {/* CONTENT OF FILE */}
            {content && content.lines && (
              <TextComponent textArr={content.lines} />
            )}
            {/*  ADJENCY MATRIX */}
            <Table
              title={" Adjency Matrix"}
              dataMatrix={content.adjencyMatrix}
              topRow={Array.from(
                { length: content.adjencyMatrix.length },
                (_, i) => i
              )}
              leftCol={Array.from(
                { length: content.adjencyMatrix.length },
                (_, i) => i
              )}
            />
          </div>
        </div>
        <div className=" w-10/12 p-10 m-auto mt-10 border-white border-2 items-center">
          {/* GRAPH SCHEME */}
          <Graph
            edges={content.edges}
            startnode={content.constraintTable[0].vertice}
            endnode={
              content.constraintTable[content.constraintTable.length - 1]
                .vertice
            }
          />
        </div>
        {/* EDGES TABLE */}
        <div className="flex justify-center mt-16">
          <BasicTable
            data={content.edges}
            title="Edge Table"
            columns={[
              { label: "From", property: "from", width: "1/3" },
              { label: "To", property: "to", width: "1/3" },
              { label: "Weight", property: "weight", width: "1/3" },
            ]}
          />
          {/* Constraint table */}
          <BasicTable
            data={content.constraintTable}
            title="Constraint Table"
            columns={[
              { label: "Vertice", property: "vertice", width: "auto" },
              { label: "Duration", property: "duration", width: "auto" },
              {
                label: "Constraints",
                property: "constraints",
                width: "auto",
              },
            ]}
          />
        </div>
      </div>
    </>
  );
}

export default Content;
