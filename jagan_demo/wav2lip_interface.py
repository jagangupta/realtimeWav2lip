import sys
import os
import numpy as np
import cv2
import torch
from tqdm import tqdm
import time

# Add core directory to sys.path to import from it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'core')))

from inference import Wav2LipInference
import audio

class Wav2LipHandler:
    def __init__(self, checkpoint_path, face_det_checkpoint="checkpoints/mobilenet.pth"):
        # Mock args object expected by Wav2LipInference
        class Args:
            def __init__(self):
                self.checkpoint_path = checkpoint_path
                self.face = "" # Will be set later
                self.audio = ""
                self.outfile = ""
                self.static = True
                self.fps = 25.
                self.pads = [0, 10, 0, 0]
                self.wav2lip_batch_size = 8 # Adjust based on GPU/CPU
                self.resize_factor = 1
                self.out_height = 480
                self.crop = [0, -1, 0, -1]
                self.box = [-1, -1, -1, -1]
                self.rotate = False
                self.nosmooth = False
                self.img_size = 96
        
        self.args = Args()
        self.inference = Wav2LipInference(self.args)
        
    def process(self, audio_path, image_path):
        """
        Generator that yields JPEG bytes of the animated frames.
        """
        if not os.path.isfile(audio_path):
            raise ValueError(f"Audio file not found: {audio_path}")
        if not os.path.isfile(image_path):
            raise ValueError(f"Image file not found: {image_path}")

        # Load Audio
        wav = audio.load_wav(audio_path, 16000)
        mel = audio.melspectrogram(wav)
        
        if np.isnan(mel.reshape(-1)).sum() > 0:
             raise ValueError('Mel contains nan! Using a TTS voice? Add a small epsilon noise to the wav file and try again')

        # Create mel chunks
        mel_chunks = []
        mel_step_size = 16
        mel_idx_multiplier = 80./self.args.fps
        i = 0
        while 1:
            start_idx = int(i * mel_idx_multiplier)
            if start_idx + mel_step_size > len(mel[0]):
                mel_chunks.append(mel[:, len(mel[0]) - mel_step_size:])
                break
            mel_chunks.append(mel[:, start_idx : start_idx + mel_step_size])
            i += 1

        print(f"Length of mel chunks: {len(mel_chunks)}")

        # Load Image
        frame = cv2.imread(image_path)
        if frame is None:
             raise ValueError(f"Could not load image: {image_path}")
        
        # Resize/Crop logic from inference.py main
        aspect_ratio = frame.shape[1] / frame.shape[0]
        frame = cv2.resize(frame, (int(self.args.out_height * aspect_ratio), self.args.out_height))
        
        y1, y2, x1, x2 = self.args.crop
        if x2 == -1: x2 = frame.shape[1]
        if y2 == -1: y2 = frame.shape[0]
        frame = frame[y1:y2, x1:x2]

        full_frames = [frame] # Static image, so just one frame repeated effectively

        # Face Detection (Cached for static image)
        # We need to pass a list of frames.
        # The datagen expects full_frames to be at least as long as mel_chunks if it was video, 
        # but for static it handles it.
        
        # However, Wav2LipInference.datagen uses self.face_detect_cache_result if static is True
        # So we need to populate it.
        self.inference.args.static = True
        self.inference.face_detect_cache_result = self.inference.face_detect([frame])

        # Generate Data Batches
        # datagen yields (img_batch, mel_batch, frame_batch, coords_batch)
        gen = self.inference.datagen(full_frames, mel_chunks)

        for i, (img_batch, mel_batch, frames, coords) in enumerate(gen):
            
            # Inference
            if self.inference.device == 'cpu':
                img_batch = np.transpose(img_batch, (0, 3, 1, 2))
                mel_batch = np.transpose(mel_batch, (0, 3, 1, 2))
                pred = self.inference.model([mel_batch, img_batch])['output']
            else:
                img_batch = torch.FloatTensor(np.transpose(img_batch, (0, 3, 1, 2))).to(self.inference.device)
                mel_batch = torch.FloatTensor(np.transpose(mel_batch, (0, 3, 1, 2))).to(self.inference.device)
                with torch.no_grad():
                    pred = self.inference.model(mel_batch, img_batch)

            pred = pred.cpu().numpy().transpose(0, 2, 3, 1) * 255.

            # Post-process and yield
            for p, f, c in zip(pred, frames, coords):
                y1, y2, x1, x2 = c
                p = cv2.resize(p.astype(np.uint8), (x2 - x1, y2 - y1))
                
                f_copy = f.copy() # Don't modify original frame in place if reused
                f_copy[y1:y2, x1:x2] = p

                # Encode to JPEG
                _, buffer = cv2.imencode('.jpg', f_copy)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

