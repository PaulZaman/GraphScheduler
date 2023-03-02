import React from "react";
import { useEffect, useState } from "react";
import { API_URL } from "../config";

import FileHeader from "./FileHeader";
import Content from "./Content";
import Scheduler from "./Scheduler";

function File({ filename }) {
  const [content, setContent] = useState();
  const [connected, setConnected] = useState(false);
  const [selected, setSelected] = useState("content");

  useEffect(() => {
    async function fetchFiles() {
      try {
        const response = await fetch(API_URL + "files/" + filename);
        const data = await response.json();
        setContent(data);
        //console.log(data);
        setConnected(true);
      } catch (error) {
        console.error(error);
      }
    }
    fetchFiles();
  }, [filename]);

  return (
    <div className="pb-10 bg-OxforfBlue">
      <FileHeader
        setSelected={setSelected}
        selected={selected}
        filename={filename}
      />
      <div className="pt-24">
        {connected ? (
          selected === "content" ? (
            <Content content={content} />
          ) : (
            <Scheduler content={content} />
          )
        ) : (
          <h1>Not connected</h1>
        )}
      </div>
    </div>
  );
}

export default File;
