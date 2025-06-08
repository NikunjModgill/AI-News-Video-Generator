import os
from moviepy.editor import VideoFileClip, TextClip, ImageClip, CompositeVideoClip
import requests
from PIL import Image
from io import BytesIO
import tempfile
from datetime import datetime
from moviepy.config import change_settings

# Configure ImageMagick path
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

class VideoGenerator:
    def __init__(self):
        self.output_dir = 'output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_video(self, article, script_scenes):
        """
        Create a video from the article and script
        """
        try:
            # Download and save the article image
            image_path = self._download_image(article['image_url'])
            if not image_path:
                raise Exception("Failed to download article image")

            # Create base video from image
            base_clip = ImageClip(image_path).set_duration(60)  # 60 seconds base

            # Create text overlays
            text_clips = []
            for scene in script_scenes:
                timestamp = self._parse_timestamp(scene['timestamp'])
                text_clip = TextClip(
                    scene['content'],
                    fontsize=40,
                    color='white',
                    bg_color='black',
                    font='Arial-Bold',
                    size=(1920, None),
                    method='caption'
                ).set_start(timestamp).set_duration(5)  # Each text appears for 5 seconds
                text_clips.append(text_clip)

            # Combine all clips
            final_clip = CompositeVideoClip([base_clip] + text_clips)
            
            # Generate output filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.output_dir, f'news_video_{timestamp}.mp4')
            
            # Write the result to a file
            final_clip.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio=False
            )

            # Cleanup
            final_clip.close()
            if os.path.exists(image_path):
                os.remove(image_path)

            return output_path

        except Exception as e:
            print(f"Error creating video: {str(e)}")
            return None

    def _download_image(self, image_url):
        """
        Download image from URL and save to temporary file
        """
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                img.save(temp_file.name)
                return temp_file.name
        except Exception as e:
            print(f"Error downloading image: {str(e)}")
        return None

    def _parse_timestamp(self, timestamp):
        """
        Convert timestamp string (MM:SS) to seconds
        """
        try:
            minutes, seconds = map(int, timestamp.split(':'))
            return minutes * 60 + seconds
        except:
            return 0 