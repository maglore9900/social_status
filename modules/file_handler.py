
import os
import shutil
from PIL import Image

class File_Handler():
    def __init__(self, file_loc="tmp/"):
        self.file_loc = file_loc
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

    def resize_image(self, filepath, max_size):
        destination_dir = self.file_loc
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
            if original_size > max_size:
                scale_factor = (max_size / original_size) ** 0.5
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