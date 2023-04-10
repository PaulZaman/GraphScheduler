import { useState, useEffect } from "react";
import SchedulerTests from "../File/SchedulerTests";
import Scheduled from "./Scheduled";

function Scheduler({ content }) {
  const [scheduled, setScheduled] = useState(false);

  useEffect(() => {
    setScheduled(false);
  }, [content]);

  return (
    <div className="flex flex-col items-center bg-OxforfBlue pt-24 text-white">
      {!scheduled ? (
        <SchedulerTests content={content} setScheduled={setScheduled} />
      ) : (
        <Scheduled content={content} setScheduled={setScheduled} />
      )}
    </div>
  );
}

export default Scheduler;
