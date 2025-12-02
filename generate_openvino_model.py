import torch
import openvino as ov
import os
import numpy as np
import sys

# Add core to path to import models
sys.path.append(os.path.join(os.getcwd(), 'jagan_demo', 'core'))
from models import Wav2Lip

def convert_model():
    print("Starting model conversion...")
    
    # Paths
    checkpoint_path = "jagan_demo/core/checkpoints/wav2lip_gan.pth"
    output_dir = "jagan_demo/core/openvino_model"
    onnx_path = os.path.join(output_dir, "wav2lip.onnx")
    xml_path = os.path.join(output_dir, "wav2lip_openvino_model.xml")
    
    os.makedirs(output_dir, exist_ok=True)

    # 1. Load PyTorch Model
    print(f"Loading checkpoint from {checkpoint_path}...")
    model = Wav2Lip()
    checkpoint = torch.load(checkpoint_path, map_location=lambda storage, loc: storage)
    
    s = checkpoint["state_dict"]
    new_s = {}
    for k, v in s.items():
        new_s[k.replace('module.', '')] = v
    model.load_state_dict(new_s)
    model.eval()

    # 2. Export to ONNX
    print("Exporting to ONNX...")
    img_batch = torch.randn(1, 6, 96, 96)
    mel_batch = torch.randn(1, 1, 80, 16)
    
    torch.onnx.export(model,
                      (mel_batch, img_batch), 
                      onnx_path,
                      input_names = ["audio_sequences", "face_sequences"], 
                      output_names = ["output"],
                      dynamic_axes = {
                          "audio_sequences": {0: "batch_size", 1: "time_size"}, 
                          "face_sequences": {0: "batch_size", 1: "channel"}
                      })
    
    # 3. Convert to OpenVINO
    print("Converting to OpenVINO...")
    core = ov.Core()
    model_onnx = core.read_model(model=onnx_path)
    
    # Serialize to XML/BIN
    ov.save_model(model_onnx, output_model=xml_path)
    print(f"Model saved to {xml_path}")

if __name__ == "__main__":
    convert_model()
