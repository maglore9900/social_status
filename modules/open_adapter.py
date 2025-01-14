import base64
from openai import OpenAI
import os

class OpenAI_Client():
    def __init__(self, env):
        self.client = OpenAI(api_key=env('openaiAPIkey'))

    # Function to encode the image
    def _encode_image(self, image_path):
        # Normalize the path to handle spaces and other edge cases
        image_path = os.path.normpath(image_path)
        
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def tag_image(self, image_path):
        # Normalize the path
        image_path = os.path.normpath(image_path)
        
        file_type = image_path.split('.')[-1]
        base64_image = self._encode_image(image_path)
        
        response = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Suggest some hash tags for the attached piece of art so it can be found on mastodon. Only return 5 hashtags, in a single response, without newlines or commas.",
                },
                {
                "type": "image_url",
                "image_url": {
                    "url":  f"data:image/{file_type};base64,{base64_image}"
                },
                },
            ],
            }
        ],
        )

        tags = response.choices[0].message.content
        clean_tags = tags.replace('\n', ' ').replace(',', ' ')
        return(clean_tags)
    
    def desc_image(self, image_path, max_chars):
        # Normalize the path
        image_path = os.path.normpath(image_path)
        
        file_type = image_path.split('.')[-1]
        base64_image = self._encode_image(image_path)
        
        response = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"Describe the image for Alt Text Accessibility. Return a response no longer than {max_chars} characters",
                },
                {
                "type": "image_url",
                "image_url": {
                    "url":  f"data:image/{file_type};base64,{base64_image}"
                },
                },
            ],
            }
        ],
        )
        description = response.choices[0].message.content
        clean_description = description.replace('\n', ' ').replace(',', ' ')
        return(clean_description)
