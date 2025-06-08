import os
import sys
from pathlib import Path

# Get the absolute path of the current directory
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

try:
    from dotenv import load_dotenv
    from news_scraper import NewsScraper
    from script_generator import ScriptGenerator
    from video_generator import VideoGenerator
    import time
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Current directory: {current_dir}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    news_scraper = NewsScraper()
    script_generator = ScriptGenerator()
    video_generator = VideoGenerator()
    
    print("Starting AI News Video Generator...")
    
    try:
        # Get trending news
        print("Fetching trending news...")
        articles = news_scraper.get_trending_news(max_articles=3)
        
        if not articles:
            print("No articles found. Exiting...")
            return
        
        # Process each article
        for i, article in enumerate(articles, 1):
            print(f"\nProcessing article {i}/{len(articles)}: {article['title']}")
            
            # Generate script
            print("Generating video script...")
            script_scenes = script_generator.generate_script(article)
            
            if not script_scenes:
                print("Failed to generate script. Skipping article...")
                continue
            
            # Create video
            print("Creating video...")
            video_path = video_generator.create_video(article, script_scenes)
            
            if video_path:
                print(f"Video created successfully: {video_path}")
            else:
                print("Failed to create video.")
            
            # Add a small delay between processing articles
            if i < len(articles):
                time.sleep(2)
        
        print("\nAll articles processed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}") 

if __name__ == "__main__":
    main() 