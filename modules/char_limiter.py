# char_limiter.py

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.validation import Validator, ValidationError

class Char_Limiter:
    def __init__(self, ):
        """
        Initializes the CharacterLimitedInput class.

        :param max_chars: Maximum number of characters allowed.
        :param prompt_message: Custom prompt message to display to the user.
        """
        self.session = PromptSession()
        self.user_input = ''

    class LengthValidator(Validator):
        def __init__(self, max_chars):
            self.max_chars = max_chars

        def validate(self, document):
            if len(document.text) > self.max_chars:
                raise ValidationError(
                    message=f'Message exceeds {self.max_chars} characters by {len(document.text) - self.max_chars}.',
                    cursor_position=len(document.text)
                )

    def get_input(self, max_chars=280, prompt_message="Please enter your message:"):
        """
        Captures user input with real-time character count and validation.

        :return: User input string within the character limit.
        """
        validator = self.LengthValidator(max_chars)
        while True:
            # Generate dynamic prompt with character count
            def get_prompt():
                current_length = len(self.session.default_buffer.text)
                remaining = max_chars - current_length
                return HTML(
                    f'<ansiblue>{prompt_message}</ansiblue>\n'
                    f'<ansigreen>Characters used:</ansigreen> '
                    f'<b>{current_length}</b>/<b>{max_chars}</b> '
                    f'(Remaining: {remaining})\n> '
                )

            try:
                self.user_input = self.session.prompt(
                    get_prompt,
                    multiline=False,
                    validator=validator,
                    validate_while_typing=True
                )
                break  # Exit loop if input is valid
            except ValidationError as e:
                print(f'\nValidation Error: {e.message}')
                print('Please shorten your message.\n')

        return self.user_input
