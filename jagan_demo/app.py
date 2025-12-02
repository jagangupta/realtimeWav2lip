from flask import Flask, render_template, request, jsonify, Response, url_for, send_from_directory
import os
import sys
import uuid

# Import our interfaces
from tts_interface import OfflineTTS
from wav2lip_interface import Wav2LipHandler

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'temp_audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
AVATAR_PATH = os.path.join(os.path.dirname(__file__), 'static', 'images', 'einstein.jpg')

# Initialize Models
print("Initializing TTS...")
tts_engine = OfflineTTS()

print("Initializing Wav2Lip...")
# Checkpoints are now in jagan_demo/core/checkpoints
CHECKPOINT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'core', 'checkpoints', 'wav2lip_gan.pth'))

if not os.path.exists(CHECKPOINT_PATH):
    print("\n" + "="*60)
    print("CRITICAL ERROR: Model checkpoint not found!")
    print(f"Missing file: {CHECKPOINT_PATH}")
    print("Please download 'wav2lip_gan.pth' and place it in 'jagan_demo/core/checkpoints/'.")
    print("See README.md for download links.")
    print("="*60 + "\n")
    sys.exit(1)

wav2lip_engine = Wav2LipHandler(CHECKPOINT_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prepare_audio', methods=['POST'])
def prepare_audio():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Generate Audio
        audio_path = tts_engine.generate_audio(text, UPLOAD_FOLDER)
        audio_filename = os.path.basename(audio_path)
        
        return jsonify({'audio_id': audio_filename})
    except Exception as e:
        print(f"Error generating audio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_audio/<audio_id>')
def get_audio(audio_id):
    return send_from_directory(UPLOAD_FOLDER, audio_id)

@app.route('/stream_video')
def stream_video():
    audio_id = request.args.get('audio_id')
    if not audio_id:
        return "No audio_id provided", 400
    
    audio_path = os.path.join(UPLOAD_FOLDER, audio_id)
    if not os.path.exists(audio_path):
        return "Audio file not found", 404
    
    def generate():
        # Process using Wav2Lip
        # We use the default avatar
        try:
            for frame in wav2lip_engine.process(audio_path, AVATAR_PATH):
                yield frame
        except Exception as e:
            print(f"Error during streaming: {e}")
            
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
