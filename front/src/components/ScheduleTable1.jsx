import React from "react";

function ScheduleTable({ schedule }) {
  const columns = Object.keys(schedule)
    .filter((key) => key !== "vertices")
    .map((key) => ({ label: key, property: key }));
  const rows = schedule.vertices;

  return (
    <div className="flex justify-center items-center h-auto bg-OxforfBlue">
      <div className="w-2/3 bg-OxforfBlue">
        <div className="text-BatteryChargedBlue font-bold text-lg text-center mb-3">
          <a>Table Title</a>
        </div>
        <table className="table-fixed w-full border border-BatteryChargedBlue">
          <thead className="bg-BatteryChargedBlue">
            <tr>
              <th className="w-1/3 px-4 py-2 text-white font-bold">Name</th>
              {columns.map((column) => (
                <th
                  key={column.label}
                  className={`w-${column.width} px-4 py-2 text-white font-bold`}
                >
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr
                key={row}
                className={`border-b border-gray-200 ${
                  row % 2 === 0 ? "bg-EgyptianBlue" : "bg-OxforfBlue"
                }`}
              >
                <td className="px-4 py-2 text-lg border text-center border-BatteryChargedBlue text-white">{`Vertex ${row}`}</td>
                {columns.map((column) => (
                  <td
                    key={`${column.label}-${row}`}
                    className="px-4 py-2 text-lg border text-center border-BatteryChargedBlue text-white"
                  >
                    {Array.isArray(schedule[column.property][row])
                      ? schedule[column.property][row].join(", ")
                      : schedule[column.property][row]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ScheduleTable;
