import os
import abc
import pyttsx3
import uuid

class TTSInterface(abc.ABC):
    @abc.abstractmethod
    def generate_audio(self, text, output_dir):
        """
        Generates audio from text and saves it to the output_dir.
        Returns the path to the generated audio file.
        """
        pass

class OfflineTTS(TTSInterface):
    def __init__(self):
        self.engine = pyttsx3.init()
        # Set properties (optional)
        self.engine.setProperty('rate', 150)    # Speed percent (can go over 100)
        self.engine.setProperty('volume', 0.9)  # Volume 0-1

    def generate_audio(self, text, output_dir):
        filename = f"{uuid.uuid4()}.wav"
        output_path = os.path.join(output_dir, filename)
        
        # Saving to file
        self.engine.save_to_file(text, output_path)
        self.engine.runAndWait()
        
        return output_path
