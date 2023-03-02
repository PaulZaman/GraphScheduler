function Table({ title, dataMatrix, topRow, leftCol }) {
  return (
    <div className="flex justify-center items-center w-full h-auto bg-OxforfBlue pt-14 pl-10">
      <div className="border-collapse text-center">
        <a className="text-BatteryChargedBlue font-bold text-lg">{title}</a>
        <div className="flex bg-BatteryChargedBlue text-white font-bold mt-4">
          <div className="p-2 border border-BatteryChargedBlue w-auto text-center"></div>
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
            className={`flex ${
              i % 2 === 0 ? "bg-EgyptianBlue" : "bg-OxforfBlue"
            }`}
          >
            <div className="p-2 border border-BatteryChargedBlue w-12 font-bold bg-BatteryChargedBlue text-center text-black">
              {leftCol[i]}
            </div>
            {row.map((cell, j) => (
              <div key={j}>
                <div className="p-2 border border-BatteryChargedBlue w-12 text-center text-white">
                  <div className={`${cell == 1 ? "" : "text-black"}`}>
                    {cell}
                  </div>
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
