/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      1: '#160f29',
      2: '#a288e3',
      3: '#BBD5ED',
      4: '#CEFDFF',
      5: '#CCFFCB',
      "red": "#f00",
      "black": "#000",
      "white": "#fff",
      "BirghtTurquoise": "#00FFFF",
      "BatteryChargedBlue": "#18A2D9",
      "EgyptianBlue": "#1034A6",
      "LighterEgyptianBlue": "#1E56A0",
      "OxforfBlue": "#081950",
      "BatteryChargedGreen": "#00FF00",
    },
  },
  plugins: [],
}