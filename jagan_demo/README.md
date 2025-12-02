# Jagan Demo - Offline Wav2Lip Avatar

This project is a standalone, offline demonstration of a real-time lip-syncing avatar system. It integrates Text-to-Speech (TTS) with the Wav2Lip deep learning model to animate a static face image based on generated audio.

## 🌟 Features
- **Fully Offline**: No internet connection required for TTS or inference.
- **Standalone**: Contains all necessary models and dependencies within the `core` folder.
- **Pluggable Architecture**: Designed with modular interfaces to easily swap TTS engines or animation models.
- **Modern UI**: Clean, responsive web interface built with Flask and Vanilla JS.

## 🏗️ Architecture

The project follows a modular design to ensure separation of concerns:

```
jagan_demo/
├── app.py                 # 🚀 Main Flask Application (Orchestrator)
├── tts_interface.py       # 🗣️ TTS Abstraction Layer
├── wav2lip_interface.py   # 👄 Wav2Lip Abstraction Layer
├── core/                  # 📦 Core Dependencies (Models, Inference Logic)
│   ├── checkpoints/       # Pre-trained weights (Wav2Lip, Face Detection)
│   ├── models/            # Model architectures
│   └── inference.py       # Original inference logic
├── static/                # 🎨 Frontend Assets (CSS, JS, Images)
└── templates/             # 📄 HTML Templates
```

### Pluggable Architecture (How to Change Components)

The system is built on interfaces, allowing you to swap components without rewriting the entire app.

#### 1. Swapping the TTS Engine
Currently, `tts_interface.py` uses `pyttsx3` (offline, robotic). To use a better engine (e.g., ElevenLabs, EdgeTTS):
1.  Open `tts_interface.py`.
2.  Create a new class inheriting from `TTSInterface`.
3.  Implement the `generate_audio(text, output_dir)` method.
4.  Update `app.py` to instantiate your new class:
    ```python
    # app.py
    # from tts_interface import MyNewTTS
    # tts_engine = MyNewTTS()
    ```

#### 2. Swapping the Animation Model
The `wav2lip_interface.py` wraps the complex inference logic. To use a different model (e.g., SadTalker, VideoReTalking):
1.  Create a new interface file (e.g., `sadtalker_interface.py`).
2.  Implement a `process(audio_path, image_path)` generator that yields JPEG frames.
3.  Update `app.py` to use this new handler.

## 🧠 Models Involved

1.  **Text-to-Speech**: `pyttsx3` (Uses OS native speech drivers).
2.  **Lip Sync**: `Wav2Lip GAN` (Generative Adversarial Network for high-quality lip synchronization).
3.  **Face Detection**: `MobileNet` (Used by Wav2Lip to crop and align the face).

## 🛠️ Setup & Installation

1.  **Prerequisites**:
    - Python 3.7+
    - NVIDIA GPU (Recommended for speed) or CPU (Slower but works).

2.  **Download Model Weights**:
    The model weights are too large to be included in the repository and must be downloaded separately.
    
    *   **Wav2Lip GAN**: [Download Link](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA?e=n9ljGW)
        -   Download and rename to `wav2lip_gan.pth`.
        -   Place it in `jagan_demo/core/checkpoints/`.
        
    *   **Face Detection (MobileNet)**: [Download Link](https://drive.google.com/drive/u/0/folders/1BopYvKEVgPK23t3rAR1kBge77N9NlP7p)
        -   Download `mobilenet.pth`.
        -   Place it in `jagan_demo/core/checkpoints/`.

3.  **Install Dependencies**:
    Navigate to the `jagan_demo` directory and run the setup script to create a virtual environment and install everything automatically:
    ```bash
    python setup_env.py
    ```
    
    Alternatively, you can manually install:
    ```bash
    pip install -r requirements.txt
    pip install pyttsx3
    ```

## 🚀 How to Run

1.  Navigate to the root directory:
    ```bash
    cd c:\Users\Jagan\Desktop\git\realtimeWav2lip
    ```
2.  Run the demo:
    ```bash
    python jagan_demo/app.py
    ```
3.  Open your browser:
    Go to `http://localhost:5000`

## 🗺️ Roadmap & Improvements

- [ ] **Better TTS**: Integrate `edge-tts` (free, high quality) or `Coqui TTS` for more natural voices.
- [ ] **Face Restoration**: Add a post-processing step (like GFPGAN) to sharpen the face after animation.
- [ ] **Real-time Streaming**: Optimize the pipeline to stream audio chunks directly to Wav2Lip instead of waiting for the full file generation.
- [ ] **Voice Cloning**: Allow users to upload a reference audio to clone voices.

## 📄 License
MIT License (inherited from the root project).
