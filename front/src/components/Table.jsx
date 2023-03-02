import React from "react";

function Table({ title, dataMatrix, topRow, leftCol }) {
  return (
    <div className="flex justify-center items-center w-auto h-auto bg-OxfordBlue pt-14 ">
      <div className="border-collapse text-center w-auto items-center">
        <a className="text-BatteryChargedBlue font-bold text-lg w-auto">
          {title}
        </a>
        <div className="flex bg-BatteryChargedBlue text-white font-bold mt-4 w-min">
          <div className="p-2 border border-BatteryChargedBlue w-12 font-bold bg-BatteryChargedBlue text-center"></div>
          {topRow.map((cell, i) => (
            <div
              key={i}
              className="p-2 border border-BatteryChargedBlue w-12 text-center text-black"
            >
              {cell}
            </div>
          ))}
        </div>
        {dataMatrix.map((row, i) => (
          <div
            key={i}
            className={`flex w-min ${
              i % 2 === 0 ? "bg-EgyptianBlue" : "bg-OxfordBlue"
            }`}
          >
            <div className="p-2 border border-BatteryChargedBlue w-12 font-bold bg-BatteryChargedBlue text-center text-black">
              {leftCol[i]}
            </div>
            {row.map((cell, j) => (
              <div key={j}>
                <div
                  className={`p-2 border border-BatteryChargedBlue w-12 text-center ${
                    cell === "1" ? "text-white" : "text-black"
                  }`}
                >
                  {cell}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Table;
