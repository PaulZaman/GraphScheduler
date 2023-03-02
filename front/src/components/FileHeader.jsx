import textLogo from "../assets/text-format.png";
import scheduleLogo from "../assets/calendar.png";

function FileHeader({ setSelected, selected, filename }) {
  const scheduleButtonStyle = `flex items-center p-3 pr-10 pl-10 hover:bg-LighterEgyptianBlue rounded-br-full bg-${
    selected === "content" ? "OxforfBlue" : "EgyptianBlue"
  }`;

  const contentButtonStyle = `flex items-center p-3 pr-10 pl-10 hover:bg-LighterEgyptianBlue bg-${
    selected === "scheduling" ? "OxforfBlue" : "EgyptianBlue"
  }`;
  return (
    <div className="flex justify-center">
      <div className="flex justify-center text-white items-center mt-16 fixed w-auto bg-OxforfBlue rounded-bl-full rounded-br-full border-b-2 ">
        <div className="text-white text-bold text-2xl pr-10 pl-10">
          FILE : {filename}
        </div>
        <div
          className={contentButtonStyle}
          onClick={() => {
            setSelected("content");
          }}
        >
          <img
            src={textLogo}
            alt="text"
            className="h-8 mr-4 cursor-pointer hover:scale-110 transition duration-300 ease-in-out"
          />
          <span>Content</span>
        </div>
        <div
          className={scheduleButtonStyle}
          onClick={() => {
            setSelected("scheduling");
          }}
        >
          <span>Scheduling</span>
          <img
            src={scheduleLogo}
            alt="text"
            className="h-8 ml-4 cursor-pointer hover:scale-110 transition duration-300 ease-in-out"
          />
        </div>
      </div>
    </div>
  );
}

export default FileHeader;
