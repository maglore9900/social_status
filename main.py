from modules import blue, masto
import environ
import os

env = environ.Env()
environ.Env.read_env()

b = blue.Blue(env)
m = masto.Mastodon_Status(env)



def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/Mac
    else:
        os.system('clear')


clear_screen()

# with open("tea2.jpg", 'rb') as f:
#     f.read()        
#     b.post("Ponder the tea eternal", f, "man confused by tea")

# b.post("yet another test, sorry for the spam")

# m.status_post("Sword Memory by Alexey Egorov\nOne of my fav artists.", "sword_memory.jpg")

while True:
    print("---- Social Status ----")
    decision = input("Post on:\n1) Mastodon\n2) Bluesky\n3) Both\n")
    if decision == "1":
        message = input("Status:\n")
        image = input("Image:\n")
        status = m.status_post(message, image)
        print(status)
        input("Press Enter to continue.")
        clear_screen()
    elif decision == "2":
        message = input("Status:\n")
        image = input("Image:\n") 
        image_desc = input("Image Description:\n")
        status = b.post(message, image, image_desc)
        print(status)
        input("Press Enter to continue.")
        clear_screen()
    elif decision == "3":
        essage = input("Status:\n")
        image = input("Image:\n") 
        image_desc = input("Image Description:\n")
        m_status = m.status_post(message, image)
        b_status = b.post(message, image, image_desc)
        print(f"Mastodon: {m_status}\nBluesky: {b_status}")
        input("Press Enter to continue.")
        clear_screen()