from modules import blue, masto, char_limiter, open_adapter, file_handler
cl = char_limiter.Char_Limiter()

max_chars = 200
tags = ''
result = cl.get_input(max_chars=max_chars, prompt_message="Status:", default=tags)
print(result)

