from modules import blue, masto
import environ

env = environ.Env()
environ.Env.read_env()

b = blue.Blue(env)
m = masto.Mastodon_Status(env)


# with open("tea2.jpg", 'rb') as f:
#     f.read()        
#     b.post("Ponder the tea eternal", f, "man confused by tea")

# b.post("yet another test, sorry for the spam")

m.status_post("Sword Memory by Alexey Egorov\nOne of my fav artists.", "sword_memory.jpg")