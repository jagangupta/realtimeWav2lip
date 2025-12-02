# Jagan Demo Walkthrough (Standalone)

The **Jagan Demo** is a fully standalone, offline application that demonstrates:
1.  **Text-to-Speech (TTS)**: Converts user text to audio using `pyttsx3` (offline).
2.  **Wav2Lip Animation**: Animates a static avatar to match the generated audio.
3.  **Modern UI**: A clean, responsive web interface.

## Prerequisites
- Python 3.x
- `pip install -r requirements.txt` (if not already done)
- `pip install pyttsx3` (already installed)

## How to Run
1.  Open a terminal in `c:\Users\Jagan\Desktop\git\realtimeWav2lip`.
2.  Run the Flask app:
    ```bash
    python jagan_demo/app.py
    ```
3.  Open your browser and navigate to:
    `http://localhost:5000`

## Usage
1.  **Type Text**: Enter any text in the text area (e.g., "Hello, this is a test of the offline lip sync system.").
2.  **Click Speak**: The system will generate audio and stream the animated video.
3.  **Watch**: The avatar will speak your text!

## Architecture
- **`jagan_demo/app.py`**: The main Flask server.
- **`jagan_demo/core/`**: Contains all Wav2Lip dependencies (`inference.py`, `models`, `checkpoints`, etc.), making the demo standalone.
- **`jagan_demo/tts_interface.py`**: Handles offline text-to-speech.
- **`jagan_demo/wav2lip_interface.py`**: Wraps the Wav2Lip inference logic.
- **`jagan_demo/static/`**: Contains the UI assets (CSS, JS, Avatar).

## Notes
- The avatar is currently set to `jagan_demo/static/images/avatar_vector.png`.
- The TTS voice is the system default (robotic). You can configure `pyttsx3` in `tts_interface.py` to change voices if your OS has others installed.
