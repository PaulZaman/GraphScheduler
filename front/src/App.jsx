import Header from "./components/Header";
import About from "./components/About";
import File from "./components/File/File";
import React, { useEffect, useState } from "react";

function App() {
  const [openedFile, setOpenedFile] = useState(null);
  const [popupisOpen, setPopupisOpen] = useState(false);

  return (
    <div className="App">
      <Header
        setOpenedFile={setOpenedFile}
        popupisOpen={popupisOpen}
        setPopupisOpen={setPopupisOpen}
      />
      <div id="content" className="bg-OxforfBlue h-screen">
        {openedFile ? (
          <File filename={openedFile} />
        ) : (
          <About popupisOpen={popupisOpen} />
        )}
      </div>
    </div>
  );
}

export default App;
