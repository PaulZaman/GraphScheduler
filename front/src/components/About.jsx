import React from "react";
import { FaReact } from "react-icons/fa";
import arrow from "../assets/curve-arrow.png";

function About({ popupisOpen }) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-4">
      {!popupisOpen && (
        <div className="w-auto h-auto flex items-center justify-center absolute top-20 left-4 scale-animation">
          <img src={arrow} alt="logo" className="w-20" />
          <a className="text-5 font-bold ml-2">Start by opening up a file</a>
        </div>
      )}
      <div className="w-2/5">
        <div className="text-3xl font-bold text-2 mb-4 flex items-center text-center">
          <FaReact className="mr-2" />{" "}
          <p className="ml-24">React Graph Scheduler</p>
        </div>
        <p className="text-lg text-center mb-4">
          This is a graph scheduler app built with React. It allows you to open
          Graphs, view their content, and perform scheduling and calculation to
          obtain different types of matrices from them. The backend end is built
          with python and flask.
        </p>
        <div className="border-t border-5 w-full my-4" />
        <div className="text-lg text-center mb-4">
          <p className="font-bold mb-2 text-2">Features:</p>
          <ul className="list-disc list-inside">
            <li>Open and view Graph files</li>
            <li>Perform scheduling and calculation on Graphs</li>
          </ul>
        </div>
        <div className="border-t border-5 w-full my-4" />
        <div className="text-lg text-center mb-4">
          <p className="font-bold mb-2 text-2">Technologies used:</p>
          <ul className="list-disc list-inside">
            <li>React</li>
            <li>Tailwind CSS</li>
            <li>Python</li>
          </ul>
        </div>
        <div className="border-t border-5 w-full my-4" />
        <div className="text-lg text-center">
          <p>
            Made with ❤️ by{" "}
            <a href="https://example.com">
              Benjamin Rossignol - Matthieu Vichet - Paul Zamanian
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default About;
