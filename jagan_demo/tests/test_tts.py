import sys
import os
import unittest

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tts_interface import OfflineTTS

class TestTTS(unittest.TestCase):
    def test_generate_audio(self):
        print("Testing TTS generation...")
        tts = OfflineTTS()
        output_dir = "tests/output"
        os.makedirs(output_dir, exist_ok=True)
        
        text = "This is a test of the text to speech system."
        output_path = tts.generate_audio(text, output_dir)
        
        print(f"Audio generated at: {output_path}")
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(os.path.getsize(output_path) > 0)
        print("TTS Test Passed!")

if __name__ == '__main__':
    unittest.main()
