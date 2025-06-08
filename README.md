# AI-News-Video-Generator

This application automatically generates short videos from trending news articles using AI. It scrapes trending news, generates scripts using GPT, and creates engaging videos with text overlays and images.

## Features

- Fetches trending news articles using NewsAPI
- Generates engaging scripts using OpenAI's GPT
- Creates 30-60 second videos with text overlays and images
- Automatically saves generated videos

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```
NEWS_API_KEY=your_news_api_key
OPENAI_API_KEY=your_openai_api_key
```

3. Run the application:
```bash
python main.py
```

## Project Structure

- `main.py`: Main application entry point
- `news_scraper.py`: Handles news fetching and processing
- `script_generator.py`: Generates video scripts using GPT
- `video_generator.py`: Creates videos from scripts
- `utils.py`: Utility functions

## Requirements

- Python 3.8+
- NewsAPI account (free tier available)
- OpenAI API key
- FFmpeg (for video processing)

## Output

The application generates videos in the `output` directory with the following format:
- Filename: `news_video_YYYYMMDD_HHMMSS.mp4`
- Duration: 30-60 seconds
- Resolution: 1920x1080 
