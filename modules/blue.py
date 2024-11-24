from atproto import Client



class Blue():
    def __init__(self, env):
        self.env = env
        self.client = Client()
        self.client.login(self.env('bsky_handle'), self.env('bsky_pass'))
    
    def post(self, message, file=None, image_desc=None):
        try: 
            if file:
                post = self.client.send_image(text=message, image=file, image_alt=image_desc)
            else:
                post = self.client.send_post('Hello world! This is a test.')
        except Exception as e:
            print("Error sending post:", str(e))


