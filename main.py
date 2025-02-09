from modules import blue, masto, char_limiter, open_adapter, file_handler
import environ
import os

env = environ.Env()
environ.Env.read_env()

b = blue.Blue(env)
m = masto.Mastodon_Status(env)
cl = char_limiter.Char_Limiter()
f = file_handler.File_Handler()

#! Conditional setup Tag Assist and Test key
tag_assist = str(env("ai_tag_assist")).lower()
if tag_assist == 'true':
    if env("openaiAPIkey") != '' or env("openaiAPIkey") != None:
        try:
            o = open_adapter.OpenAI_Client(env)
            tag_assist = True
        except Exception as e:
            print(f"Failed to enable AI Tag Assist: {e}")
            tag_assist = False
else:
    tag_assist = False

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/Mac
    else:
        os.system('clear')
        
def post_to_platform(platform_name, max_chars, has_image_desc=False):
    """
    Handles posting a message to a specified platform.
    """
    clear_screen()
    if tag_assist:
        print("   *AI Tag Assist Enabled")
    image = input("Attach Image (optional):\n")
    tags = f"Artist: Unknown\n{o.tag_image(image)}" if tag_assist and image else None
    message = cl.get_input(max_chars=max_chars, prompt_message="Status:", default=tags)
    image_desc = cl.get_input(max_chars=300, prompt_message="Image Description:") if has_image_desc and image else ''

    if platform_name == "mastodon":
        return m.status_post(message, image)
    elif platform_name == "bluesky":
        return b.post(message, image, image_desc)
    else:
        raise ValueError(f"Unknown platform: {platform_name}")

def post_to_multiple(platforms, max_chars):
    """
    Handles posting a message to multiple platforms.
    """
    clear_screen()
    #! handle user input and tag_assist
    if tag_assist: print("   *AI Tag Assist Enabled")
    image = input("Attach Image (optional):\n")
    if image: image = os.path.normpath(image.strip('\"'))
    tags = f"Artist: Unknown\n{o.tag_image(image)}" if tag_assist and image else None
    message = cl.get_input(max_chars=max_chars, prompt_message="Status:", default=tags)
    # image_desc = cl.get_input(max_chars=300, prompt_message="Image Description:") if image else ''
    if image:
        image_desc = cl.get_input(max_chars=max_chars, prompt_message="Image Description:",
            default=o.desc_image(image, max_chars=max_chars) if tag_assist and image else '')
    else:
        image_desc = ''

    statuses = {}
    for platform in platforms:
        if platform == "mastodon":
            statuses["Mastodon"] = m.status_post(message, image)
        elif platform == "bluesky":
            statuses["Bluesky"] = b.post(message, image, image_desc)
        else:
            raise ValueError(f"Unknown platform: {platform}")

    return statuses

def main():
    platforms = {
        "1": {"name": "mastodon", "max_chars": 500, "has_image_desc": False},
        "2": {"name": "bluesky", "max_chars": 300, "has_image_desc": True},
    }

    # Calculate smallest max_chars value across all platforms
    smallest_max_chars = min(platform["max_chars"] for platform in platforms.values())

    # Add the "all" option dynamically
    platforms["3"] = {"name": "all", "max_chars": smallest_max_chars, "has_image_desc": True}

    while True:
        clear_screen()
        print("---- Social Status ----")
        decision = input("Post on:\n   1) Mastodon\n   2) Bluesky\n   3) All\n")
        platform_info = platforms.get(decision)

        if not platform_info:
            print("Invalid selection. Please try again.")
            input("Press Enter to continue.")
            continue

        if platform_info["name"] == "all":
            statuses = post_to_multiple(["mastodon", "bluesky"], max_chars=smallest_max_chars)
            print("\n".join([f"{k}: {v}" for k, v in statuses.items()]))
        else:
            status = post_to_platform(
                platform_name=platform_info["name"],
                max_chars=platform_info["max_chars"],
                has_image_desc=platform_info["has_image_desc"],
            )
            print(status)
        #! remove all tmp files from the tmp/ dir
        f.file_cleanup()
        input("Press Enter to continue.")

if __name__ == "__main__":
    main()
