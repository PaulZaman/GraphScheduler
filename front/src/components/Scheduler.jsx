import { useState } from "react";
import SchedulerTests from "./SchedulerTests";
import Scheduled from "./Scheduled";

function Scheduler({ content }) {
  const [scheduled, setScheduled] = useState(false);
  return (
    <div className="flex flex-col items-center bg-OxforfBlue pt-24 text-white">
      {!scheduled ? (
        <SchedulerTests content={content} setScheduled={setScheduled} />
      ) : (
        <Scheduled setScheduled={setScheduled} />
      )}
    </div>
  );
}

export default Scheduler;
