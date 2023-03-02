import React, { useState, useEffect } from "react";
import { API_URL } from "../config";

function FileListPopup({ setPopupisOpen, setOpenedFile }) {
  const [connected, setConnected] = useState(false);
  const [files, setFiles] = useState([]);

  useEffect(() => {
    if (files.length === 0) {
      console.log("No files found");
      setConnected(false);
    } else {
      setConnected(true);
    }
  }, [files]);

  const handleClick = (file) => {
    setOpenedFile(file);
    setPopupisOpen(false);
  };

  useEffect(() => {
    async function fetchFiles() {
      try {
        const response = await fetch(API_URL + "files");
        const data = await response.json();
        setFiles(data.files);
      } catch (error) {
        console.error(error);
      }
    }

    fetchFiles();
  }, []);

  return (
    <div className="fixed left-0 w-full h-full bg-gray-800 bg-opacity-50 flex top-16 z-1">
      <div className="bg-white w-1/4 h-5/6 rounded-lg shadow-lg">
        <div className="bg-3 h-12 p-1 flex items-center">
          <h1 className="text-2xl font-bold text-gray-800 flex-1 text-center rounded-xl">
            Open File
          </h1>
        </div>
        <div className="h-full overflow-y-auto">
          <>
            {files.map((el) => (
              <div
                key={el.id}
                className="h-16 flex bg-gradient-to-r from-EgyptianBlue to-BatteryChargedBlue items-center justify-between px-4 border-b border-gray-300"
              >
                <h1 className="text-xl font-bold text-gray-800">{el.file}</h1>
                <button
                  className="bg-4 text-black px-4 py-2 rounded-lg"
                  onClick={() => handleClick(el.file)}
                >
                  Open
                </button>
              </div>
            ))}
            {!connected && (
              <div className="">
                <h1 className="text-2 text-2xl m-2 text-center mt-5">
                  Could not connect to server
                </h1>
              </div>
            )}
          </>
        </div>
      </div>
    </div>
  );
}

export default FileListPopup;
