
import os
import shutil
from PIL import Image

class File_Handler():
    def __init__(self, file_loc="tmp/"):
        self.file_loc = file_loc
    # def normalize_path(self, path):
    #     """
    #     Ensures the path is correctly formatted for Python.
    #     """
    #     # If the path starts with two backslashes (UNC path),
    #     # Use a raw string or escape the backslashes
    #     if path.startswith('\\\\') or path.startswith(r'\\'):
    #         # Normalize using raw strings to handle UNC paths correctly
    #         normalized_path = os.path.normpath(path)
    #     else:
    #         normalized_path = os.path.normpath(path)
        
    #     return normalized_path



    def normalize_path(self, path):
        """
        Ensures the path is correctly formatted for Python.
        If the path contains spaces, the file is copied to a temporary directory.
        """
        # Normalize the initial path
        normalized_path = os.path.normpath(path)
        # Check if the path contains spaces
        if ' ' in normalized_path:
            # Ensure 'tmp' directory exists
            temp_dir = "tmp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            # Get the filename from the path
            filename = os.path.basename(normalized_path)
            # Define the new path in the temp directory
            temp_path = os.path.join(temp_dir, filename)
            try:
                # Copy the file to the temporary directory
                shutil.copy2(normalized_path, temp_path)
                # Update the normalized path to the new temporary path
                normalized_path = temp_path
            except (IOError, OSError) as e:
                print(f"Error copying file: {e}")
                # Handle the error, e.g., re-raise or log
                raise
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
            
    def file_cleanup(self):
        #! file clean up
        if os.path.exists(self.file_loc):
            for filename in os.listdir(self.file_loc):
                file_path = os.path.join(self.file_loc, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")