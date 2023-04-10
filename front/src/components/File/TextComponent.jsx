import { useState, useEffect } from "react";

function TextComponent({ textArr }) {
  const [text, setText] = useState(textArr.join("\n"));

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  useEffect(() => {
    setText(textArr.join("\n"));
  }, [textArr]);

  return (
    <>
      <div className="flex flex-col justify-center items-center w-full h-auto bg-OxforfBlue mr-10">
        <div className="text-BatteryChargedBlue font-bold text-lg mt-16 mb-4 text-center">
          <a>Content of file</a>
        </div>
        <div className="w-full flex justify-center items-center h-auto bg-OxforfBlue">
          <div className="bg-white w-full rounded-lg p-4 shadow-md">
            <textarea
              readonly
              value={text}
              className="resize-none block w-full h-96 p-2 text-2xl text-black rounded-lg border border-BatteryChargedBlue focus:outline-none focus:ring focus:ring-BatteryChargedBlue"
            />
          </div>
        </div>
      </div>
    </>
  );
}

export default TextComponent;
