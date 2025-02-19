from msvcrt import getwch
from random import sample
from json import load
from os import path

# Function to get the absolute path to the JSON files
def get_file_path(filename):
    # Assuming the JSON files are in the same directory as the script
    script_dir = path.dirname(path.abspath(__file__))
    return path.join(script_dir, filename)

# Game settings function
def game_settings():
    print("Enter language of test (ru, eng): ")
    lang = input().strip().lower()
    if lang in ["ru", "eng"]:
        return lang
    else:
        print("Invalid language. Please enter 'ru' or 'eng'.")
        return False

# Generation the number of words specified
def wordGen(lang, count):
    try:
        if lang == 'eng':
            with open(get_file_path("wordlist.json"), "r", encoding="utf-8") as file:
                words = load(file)
        elif lang == 'ru':
            with open(get_file_path("russian-words.json"), "r", encoding="utf-8") as file:
                words = load(file)
        else:
            return False
        
        random_words = sample(words, count)
        result = " ".join(random_words)
        return result
    except FileNotFoundError:
        print(f"Error: File not found for language '{lang}'.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def typing_test():
    lang = game_settings()
    if not lang:
        return  # Exit the function if language is invalid

    while True:
        try:
            word_count = int(input("Enter word count: ").strip())
            if word_count <= 0:
                raise ValueError("Word count must be a non-negative number.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a positive integer.")

    target_text = wordGen(lang, word_count)
    if not target_text:
        return  # Exit the function if word generation fails

    print("Type the following text:")
    print(target_text)
    user_input = ""
    index = 0
    mistakes = 0
    backspace_char = b'\x08'  # ASCII value for backspace

    while True:
        char = getwch()  # Use getwch to handle wide characters (UTF-8)
        if char == '\r':  # Enter key
            break
        elif char == '\x08' and index > 0:  # Backspace key
            # Handle backspace
            print("\b \b", end='', flush=True)
            user_input = user_input[:-1]
            index -= 1
        elif index < len(target_text) and char == target_text[index]:
            print(char, end='', flush=True)
            user_input += char
            index += 1
        else:
            mistakes += 1  # Increment mistakes for incorrect characters
            user_input += char

    print("\n\nTyping test complete!")
    print(f"Your input: {user_input}")
    print(f"Target text: {target_text}")
    accuracy = accuracy = ((index - mistakes) / index) * 100  # Correct characters divided by total characters written
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    typing_test()
