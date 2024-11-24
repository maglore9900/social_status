from mastodon import Mastodon
import random

class Mastodon_Status():
    def __init__(self, env):
        self.env = env
        self.mastodon = Mastodon(client_id = self.env('mastodon_clientcred'),)
        self.mastodon.log_in(
            self.env('mastodon_login'),
            self.env('mastodon_pass'),
            to_file = self.env('mastodon_usercred')
        )
        self.idem_key = random.randint(1,1000000)
        
    def _media_upload(self, file, filename=None):
        result = self.mastodon.media_post(
            media_file=file, 
            mime_type=None, 
            description=None, 
            focus=None, 
            file_name=filename, 
            thumbnail=None, 
            thumbnail_mime_type=None, 
            synchronous=False)
        return(result['id'])
    
    def status_post(self, status, file=None):
        try:
            if file:
                id = self._media_upload(file, filename=None)
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
        
        
    


