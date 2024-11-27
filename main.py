from modules import blue, masto, char_limiter
import environ
import os

env = environ.Env()
environ.Env.read_env()

b = blue.Blue(env)
m = masto.Mastodon_Status(env)
cl = char_limiter.Char_Limiter()



def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/Mac
    else:
        os.system('clear')

while True:
    clear_screen()
    print("---- Social Status ----")
    decision = input("Post on:\n   1) Mastodon\n   2) Bluesky\n   3) Both\n")
    if decision == "1":
        clear_screen()
        message = cl.get_input(max_chars=500, prompt_message="Status:")
        image = input("Image:\n")
        status = m.status_post(message, image)
        print(status)
        input("Press Enter to continue.")
    elif decision == "2":
        clear_screen()
        message = cl.get_input(max_chars=300, prompt_message="Status:")
        image = input("Image:\n") 
        if image: 
            image_desc = cl.get_input(max_chars=300, prompt_message="Image Description:")
        else:
            image_desc = ''
        status = b.post(message, image, image_desc)
        print(status)
        input("Press Enter to continue.")
    elif decision == "3":
        clear_screen()
        message = cl.get_input(max_chars=300, prompt_message="Status:")
        image = input("Image:\n")
        if image: 
            image_desc = cl.get_input(max_chars=300, prompt_message="Image Description:")
        else:
            image_desc = ''
        m_status = m.status_post(message, image)
        b_status = b.post(message, image, image_desc)
        print(f"Mastodon: {m_status}\nBluesky: {b_status}")
        input("Press Enter to continue.")
