# Morse Code Converter & Game

A modern, interactive web app to convert text ↔ Morse code, play Morse sounds, and learn Morse code through a fun game and tutorial. Built with Flask and pure JavaScript.

## Features
- **Text ↔ Morse code conversion** (with sound playback)
- **Game mode**: Guess the code (Easy: letters, Medium: letters+numbers, Hard: words)
- **Tutorial**: Clickable Morse chart with sound for A–Z, 0–9
- **Dark mode** and animated background
- **Copy, clear, and responsive UI**
- **No API keys required**

## Screenshots

| Home / Converter | Game Mode | Tutorial |
|---|---|---|
| ![Home](static/screenshots/home.png) | ![Game](static/screenshots/game.png) | ![Tutorial](static/screenshots/tutorial.png) |

## Getting Started

1. **Clone the repo:**
   ```bash
   git clone https://github.com/singhmanish0665/morse-code-webapp.git
   cd morse-code-webapp
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   python app.py
   ```
4. **Open in browser:**
   Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Project Structure
```
app.py
requirements.txt
templates/
  index.html
static/
  style.css
  favicon.ico
  screenshots/
    home.png
    game.png
    tutorial.png
```

## License
MIT

---