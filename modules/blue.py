from modules import file_handler
from atproto import Client
import os




class Blue():
    def __init__(self, env):
        self.env = env
        self.client = Client()
        self.client.login(self.env('bsky_handle'), self.env('bsky_pass'))
        self.max_size = 1000000  # Max file size in bytes
        self.fl = file_handler.File_Handler()

    def post(self, message, file=None, image_desc=None):
        try:
            if file:
                file = self.fl.normalize_path(file)
                if os.path.getsize(file) > self.max_size:
                    file = self.fl.resize_image(file, self.max_size)
                with open(file, 'rb') as f:
                    file = f.read()
                    post = self.client.send_image(text=message, image=file, image_alt=image_desc)
            else:
                post = self.client.send_post(message)
            return "Success"
        except Exception as e:
            return("Error sending post:", str(e))
        
   

