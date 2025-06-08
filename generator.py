import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ScriptGenerator:
    def __init__(self):
        self.api_key = os.getenv('Add your OpenAI API key here')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=self.api_key) 

    def generate_script(self, article):
        """
        Generate a video script from an article using GPT
        """
        try:
            prompt = f"""Create a 30-60 second video script for a news article. 
            The script should be engaging, informative, and suitable for a short video format.
            Include timestamps for text overlays and scene transitions.
            
            Article Title: {article['title']}
            Article Description: {article['description']}
            Source: {article['source']}
            
            Format the response as:
            [0:00] Opening text
            [0:05] Scene description
            [0:10] Next text overlay
            And so on...
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional video script writer who creates engaging, concise scripts for news videos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            script = response.choices[0].message.content.strip()
            return self._parse_script(script)

        except Exception as e:
            print(f"Error generating script: {str(e)}")
            return None

    def _parse_script(self, script):
        """
        Parse the generated script into a structured format
        """
        scenes = []
        for line in script.split('\n'):
            if '[' in line and ']' in line:
                try:
                    timestamp = line[line.find('[')+1:line.find(']')]
                    content = line[line.find(']')+1:].strip()
                    scenes.append({
                        'timestamp': timestamp,
                        'content': content
                    })
                except:
                    continue
        return scenes 