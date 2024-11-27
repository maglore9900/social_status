from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.validation import Validator, ValidationError

# Define the maximum character limit
max_chars = 280

# Create a custom validator
class LengthValidator(Validator):
    def validate(self, document):
        if len(document.text) > max_chars:
            raise ValidationError(
                message=f'Message exceeds {max_chars} characters by {len(document.text) - max_chars}.',
                cursor_position=len(document.text)
            )

def main():
    session = PromptSession()
    while True:
        # Generate dynamic prompt with character count
        def get_prompt():
            current_length = len(session.default_buffer.text)
            remaining = max_chars - current_length
            return HTML(f'<ansiblue>Characters used:</ansiblue> <b>{current_length}</b>/<b>{max_chars}</b> (Remaining: {remaining})\n> ')

        # Get user input with real-time character count
        try:
            user_input = session.prompt(
                get_prompt,
                multiline=False,
                validator=LengthValidator(),
                validate_while_typing=True
            )
            break  # Exit loop if input is valid
        except ValidationError as e:
            print(f'\nValidation Error: {e.message}')
            print('Please shorten your message.\n')

    # Proceed with posting the message
    print("\nYour message will be posted:")
    print(user_input)
    # Add your code here to post the message to social media sites

if __name__ == '__main__':
    main()
