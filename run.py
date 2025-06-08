import os
import sys
from pathlib import Path

# Print current working directory and Python path
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Add the current directory to Python path
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

# List all files in the current directory
print("\nFiles in current directory:")
for file in os.listdir(current_dir):
    print(f"- {file}")

# Try importing the modules
print("\nTrying to import modules...")
try:
    from dotenv import load_dotenv
    print("✓ dotenv imported successfully")
except ImportError as e:
    print(f"✗ Error importing dotenv: {e}")

try:
    from news_scraper import NewsScraper
    print("✓ news_scraper imported successfully")
except ImportError as e:
    print(f"✗ Error importing news_scraper: {e}")

try:
    from script_generator import ScriptGenerator
    print("✓ script_generator imported successfully")
except ImportError as e:
    print(f"✗ Error importing script_generator: {e}")

try:
    from video_generator import VideoGenerator
    print("✓ video_generator imported successfully")
except ImportError as e:
    print(f"✗ Error importing video_generator: {e}")

# If all imports are successful, run the main script
if all(module in sys.modules for module in ['dotenv', 'news_scraper', 'script_generator', 'video_generator']):
    print("\nAll modules imported successfully. Running main script...")
    from main import main
    main()
else:
    print("\nSome modules failed to import. Please check the errors above.") 