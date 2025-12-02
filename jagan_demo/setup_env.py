import os
import sys
import subprocess
import venv

def create_venv(venv_dir):
    if os.path.exists(venv_dir):
        print(f"Virtual environment '{venv_dir}' already exists. Skipping creation.")
        return
    print(f"Creating virtual environment in {venv_dir}...")
    venv.create(venv_dir, with_pip=True)

def install_requirements(venv_dir):
    # Determine python and pip executables
    if sys.platform == "win32":
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        python_exe = os.path.join(venv_dir, "bin", "python")
        pip_exe = os.path.join(venv_dir, "bin", "pip")

    print(f"Upgrading pip using {python_exe}...")
    subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

    print("Installing dependencies...")
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        subprocess.check_call([pip_exe, "install", "-r", requirements_file])
    else:
        print("requirements.txt not found!")
    
    # Ensure pyttsx3 is installed (it might not be in the copied requirements.txt)
    subprocess.check_call([pip_exe, "install", "pyttsx3"])

    print("\nSetup complete!")
    print(f"To run the demo, activate the environment and run app.py:")
    if sys.platform == "win32":
        print(f"  {venv_dir}\\Scripts\\activate")
    else:
        print(f"  source {venv_dir}/bin/activate")
    print("  python app.py")

import webbrowser

def setup_models():
    print("\n" + "="*50)
    print("Checking for required model files...")
    print("="*50)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    checkpoints_dir = os.path.join(base_dir, "core", "checkpoints")
    os.makedirs(checkpoints_dir, exist_ok=True)

    models = {
        "wav2lip_gan.pth": "https://huggingface.co/numz/wav2lip_studio/resolve/main/Wav2lip/wav2lip_gan.pth",
        "mobilenet.pth": "https://huggingface.co/cncbec/wav2lip/resolve/main/mobilenet.pth"
    }

    missing = []
    for model_name, url in models.items():
        path = os.path.join(checkpoints_dir, model_name)
        if not os.path.exists(path):
            print(f"[-] Missing: {model_name}")
            missing.append((model_name, url))
        else:
            print(f"[+] Found: {model_name}")

    if not missing:
        print("\nAll models are present! You are ready to run the demo.")
        return

    print("\n" + "!"*60)
    print("ACTION REQUIRED: You need to download the missing models.")
    print("Automatic download is not possible for these hosting providers.")
    print("I will open the download pages for you now.")
    print("!"*60 + "\n")

    input("Press Enter to open download links...")

    for model_name, url in missing:
        print(f"Opening link for {model_name}...")
        webbrowser.open(url)
    
    print("\n" + "-"*60)
    print(f"Please download the files and place them in:\n{checkpoints_dir}")
    print("-"*60)
    
    while True:
        response = input("\nHave you placed the files? (y/n): ").lower()
        if response == 'y':
            # Re-verify
            still_missing = []
            for model_name, _ in missing:
                if not os.path.exists(os.path.join(checkpoints_dir, model_name)):
                    still_missing.append(model_name)
            
            if not still_missing:
                print("Verification successful! Setup complete.")
                break
            else:
                print(f"Still missing: {', '.join(still_missing)}")
                print("Please check the file names and location.")
        else:
            print("Waiting...")

if __name__ == "__main__":
    venv_name = "venv"
    create_venv(venv_name)
    install_requirements(venv_name)
    setup_models()
