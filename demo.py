from enum import Enum
import random
import string


def generate_password(difficulty: str, length: int = 12) -> str:
    match difficulty:
        case "MEDIUM":
            chars = string.ascii_letters + string.digits
        case "HARD":
            chars = string.ascii_letters + string.digits + string.punctuation
        case _:
            chars = string.ascii_lowercase
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# Example usage:
if __name__ == "__main__":
    print("Generated passwords:")
    for level in ["EASY", "MEDIUM", "HARD"]:
        print(f"{level} password: {generate_password(level, 10)}")
