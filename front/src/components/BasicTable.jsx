import React from "react";

function BasicTable({ data, title, columns }) {
  return (
    <>
      <div className="flex justify-center items-center h-auto bg-OxforfBlue">
        <div className="w-2/3 bg-OxforfBlue">
          <div className="text-BatteryChargedBlue font-bold text-lg text-center mb-3">
            <a>{title}</a>
          </div>
          <table className="table-fixed w-full border border-BatteryChargedBlue">
            <thead className="bg-BatteryChargedBlue">
              <tr>
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
              {data.map((item, index) => (
                <tr
                  key={index}
                  className={`border-b border-gray-200 ${
                    index % 2 === 0 ? "bg-EgyptianBlue" : "bg-OxforfBlue"
                  }`}
                >
                  {columns.map((column) => (
                    <td
                      key={`${column.label}-${item[column.property]}`}
                      className={`px-4 py-2 text-lg border text-center border-BatteryChargedBlue text-white`}
                    >
                      {Array.isArray(item[column.property])
                        ? item[column.property].join(", ")
                        : item[column.property]}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default BasicTable;
