import subprocess
import sys
import os

def install_requirements():
    """Install the requirements from requirements.txt."""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Requirements installed successfully!")

def download_spacy_models():
    """Download necessary spaCy models."""
    print("Downloading spaCy models...")
    
    # Download small model
    print("Downloading en_core_web_sm...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    
    # Download medium model
    print("Downloading en_core_web_md...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_md"])
    
    print("spaCy models downloaded successfully!")

def download_nltk_resources():
    """Download necessary NLTK resources."""
    print("Downloading NLTK resources...")
    import nltk
    resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
    for resource in resources:
        print(f"Downloading {resource}...")
        nltk.download(resource)
    print("NLTK resources downloaded successfully!")

def create_upload_directory():
    """Create necessary directories."""
    print("Creating upload directory...")
    os.makedirs(os.path.join("app", "uploads"), exist_ok=True)
    print("Directory created successfully!")

def main():
    """Main function to set up the project."""
    print("Starting setup for Smart Resume Analyzer...")
    
    try:
        install_requirements()
        download_spacy_models()
        download_nltk_resources()
        create_upload_directory()
        
        print("\nSetup completed successfully!")
        print("\nTo run the application, use the following command:")
        print("python main.py")
    except Exception as e:
        print(f"\nError during setup: {e}")
        print("Please fix the issue and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 