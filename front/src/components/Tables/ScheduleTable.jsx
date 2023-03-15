import React from "react";

function ScheduleTable({ schedule, title }) {
  const rows = Object.keys(schedule.headers).map((key) => {
    return {
      key: key,
      header: schedule.headers[key],
    };
  });

  return (
    <div className="flex justify-center items-center h-auto bg-OxforfBlue mt-16">
      <div className="w-full bg-OxforfBlue">
        <div className="text-BatteryChargedBlue font-bold text-lg text-center mb-3">
          <a>{title}</a>
        </div>
        <table className="table-fixed w-full border border-BatteryChargedBlue">
          <tbody>
            {rows.map((row) => (
              <tr
                key={row.key}
                className={`${
                  row.key % 2 === 0 ? "bg-EgyptianBlue" : "bg-OxforfBlue"
                }`}
              >
                <td className="px-4 py-2 text-lg border text-center border-BatteryChargedBlue bg-BatteryChargedBlue text-white w-52">
                  {row.header}
                </td>
                {schedule[row.header].map((item) => (
                  <td className="px-4 py-2 text-lg border text-center border-BatteryChargedBlue text-white w-auto">
                    {Array.isArray(item) ? item.join(", ") : item}
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
