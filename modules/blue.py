from atproto import Client
import os
from PIL import Image
import shutil


class Blue():
    def __init__(self, env):
        self.env = env
        self.client = Client()
        self.client.login(self.env('bsky_handle'), self.env('bsky_pass'))
        self.max_size = 1000000  # Max file size in bytes

    def post(self, message, file=None, image_desc=None):
        try:
            if file:
                file = self.normalize_path(file)
                if os.path.getsize(file) > self.max_size:
                    file = self.resize_image(file)
                with open(file, 'rb') as f:
                    file = f.read()
                    post = self.client.send_image(text=message, image=file, image_alt=image_desc)
            else:
                post = self.client.send_post(message)
            return "Success"
        except Exception as e:
            return("Error sending post:", str(e))
        
    def normalize_path(self, path):
        """
        Ensures the path is correctly formatted for Python.
        """
        # If the path starts with two backslashes (UNC path),
        # Use a raw string or escape the backslashes
        if path.startswith('\\\\') or path.startswith(r'\\'):
            # Normalize using raw strings to handle UNC paths correctly
            normalized_path = os.path.normpath(path)
        else:
            normalized_path = os.path.normpath(path)
        
        return normalized_path

    def resize_image(self, filepath):
        destination_dir = 'tmp/'
        # Ensure the destination directory exists
        os.makedirs(destination_dir, exist_ok=True)
        
        # Get the filename from the source file path
        file_name = os.path.basename(filepath)
        
        # Copy the file to the destination directory
        destination_file_path = os.path.join(destination_dir, file_name)
        shutil.copy(filepath, destination_file_path)

        # Open and process the image
        with Image.open(destination_file_path) as img:
            # Calculate scale factor based on max size and file size
            original_size = os.path.getsize(destination_file_path)
            if original_size > self.max_size:
                scale_factor = (self.max_size / original_size) ** 0.5
                new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
                print(f"Scaling image to: {new_size}")

                # Resize the image
                img = img.resize(new_size, Image.LANCZOS)

                # Save the resized image
                temp_filepath = os.path.join(destination_dir, f"{os.path.splitext(file_name)[0]}_resized{os.path.splitext(file_name)[1]}")
                img.save(temp_filepath, format=img.format)
                return temp_filepath
            else:
                return destination_file_path

