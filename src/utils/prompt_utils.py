from src.config import BASE_PATH
import os
def load_prompt_template(filename):
    """Load a prompt template from a text file."""
    filepath = os.path.join(BASE_PATH, 'src/prompts', filename)
    with open(filepath, 'r') as file:
        return file.read()