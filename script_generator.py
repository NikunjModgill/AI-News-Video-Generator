import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ScriptGenerator:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print("ScriptGenerator initialized")
    
    def generate_script(self, article):
        """
        Generate a video script from an article
        """
        print(f"\nGenerating script for article: {article['title']}")
        
        try:
            # Create the prompt for the article
            prompt = f"""
            Create a concise video script for this news article:
            Title: {article['title']}
            Description: {article['description']}
            
            Format the script as a series of scenes with timestamps.
            Each scene should be 5-10 seconds long.
            Start with a brief introduction, then cover the main points.
            End with a conclusion.
            
            Format each line as: [MM:SS] Text content
            Example:
            [00:00] Introduction text
            [00:05] Main point 1
            [00:15] Main point 2
            [00:25] Conclusion
            """

            # Generate the script using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional news script writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            # Extract and parse the script
            script_text = response.choices[0].message.content
            print("\nGenerated script:")
            print(script_text)

            # Parse the script into scenes
            scenes = []
            for line in script_text.split('\n'):
                line = line.strip()
                if line and '[' in line and ']' in line:
                    try:
                        # Extract timestamp and content
                        timestamp = line[line.find('[')+1:line.find(']')]
                        content = line[line.find(']')+1:].strip()
                        if timestamp and content:
                            scenes.append({
                                'timestamp': timestamp,
                                'content': content
                            })
                    except Exception as e:
                        print(f"Error parsing line: {line}")
                        continue

            if not scenes:
                # If no valid scenes were parsed, create a default script
                scenes = [
                    {'timestamp': '00:00', 'content': article['title']},
                    {'timestamp': '00:05', 'content': article['description']}
                ]

            return scenes

        except Exception as e:
            print(f"Error generating script: {str(e)}")
            # Return a basic script if generation fails
            return [
                {'timestamp': '00:00', 'content': article['title']},
                {'timestamp': '00:05', 'content': article['description']}
            ]

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