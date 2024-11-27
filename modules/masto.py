from modules import file_handler
from mastodon import Mastodon
import os

class Mastodon_Status():
    def __init__(self, env):
        self.env = env
        self.mastodon = Mastodon(client_id = self.env('mastodon_clientcred'),)
        self.mastodon.log_in(
            self.env('mastodon_login'),
            self.env('mastodon_pass'),
            to_file = self.env('mastodon_usercred')
        )
        self.max_size = 16000000 #in bytes
        self.fl = file_handler.File_Handler()
        
    # def _media_upload(self, file, filename=None):
    #     result = self.mastodon.media_post(
    #         media_file=file, 
    #         mime_type=None, 
    #         description=None, 
    #         focus=None, 
    #         file_name=filename, 
    #         thumbnail=None, 
    #         thumbnail_mime_type=None, 
    #         synchronous=False)
    #     return(result['id'])
    
    def _media_upload(self, file, file_name=None):
        try:
            file = self.fl.normalize_path(file)
            if os.path.getsize(file) > self.max_size:
                file = self.fl.resize_image(file, self.max_size)
            result = self.mastodon.media_post(
                media_file=file, 
                mime_type=None, 
                description=None, 
                focus=None, 
                file_name=file_name, 
                thumbnail=None, 
                thumbnail_mime_type=None, 
                synchronous=False)
            return(result['id'])
        except Exception as e:
            return("Error handling media:", str(e))
    
    def status_post(self, status, file=None):
        try:
            if file:
                id = self._media_upload(file, file_name=None)
            else:
                id = None    
            
            result = self.mastodon.status_post(
                status, 
                in_reply_to_id=None, 
                media_ids=id, 
                sensitive=False, 
                visibility=self.env('visibility'), 
                spoiler_text=None, 
                language=self.env('language'), 
                idempotency_key=None, 
                content_type=None, 
                scheduled_at=None, 
                poll=None, 
                quote_id=None)
            return "success\n"
        except Exception as e:
            return(f"failed: {e}")
        
        
    


