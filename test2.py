from modules import open_adapter
import environ

env = environ.Env()
environ.Env.read_env()


o = open_adapter.OpenAI_Client(env)

print(o.tag_image('test.jpg','jpg'))