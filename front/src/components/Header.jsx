import React, { useState } from "react";
import OpenImage from "../assets/open.png";
import Home from "../assets/home.png";
import FileListPopup from "./FileListPopup.jsx";

function Header({ setOpenedFile, popupisOpen, setPopupisOpen }) {
  const handleImageClick = () => {
    setPopupisOpen(!popupisOpen);
  };

  return (
    <div>
      <div className="flex items-center justify-between bg-gradient-to-r from-EgyptianBlue to-BatteryChargedBlue h-16 px-4 fixed w-full z-1">
        <div className="flex items-center" onClick={handleImageClick}>
          <img
            src={OpenImage}
            alt="open"
            className="h-8 mr-4 cursor-pointer hover:scale-110 transition duration-300 ease-in-out"
          />
          <h1 className="text-xl font-medium text-white cursor-pointer hover:underline transition duration-300 ease-in-out">
            Open new file
          </h1>
        </div>
        <h1 className="text-3xl font-bold text-white text-center mr-20">
          Graph Scheduler
        </h1>
        <div className="flex items-center" onClick={() => setOpenedFile(null)}>
          <h1 className="text-xl font-medium text-white mr-4 cursor-pointer hover:underline transition duration-300 ease-in-out">
            Home
          </h1>
          <img
            src={Home}
            alt="open"
            className="h-8 cursor-pointer hover:scale-110 transition duration-300 ease-in-out"
          />
        </div>
      </div>
      {popupisOpen && (
        <FileListPopup
          setOpenedFile={setOpenedFile}
          setPopupisOpen={setPopupisOpen}
        />
      )}
    </div>
  );
}

export default Header;
