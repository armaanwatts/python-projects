import random
import string

print("=== Password Generator ===")

length = int(input("Enter password length: "))

uppercase = input("Include uppercase letters? (y/n): ").lower() == "y"
lowercase = input("Include lowercase letters? (y/n): ").lower() == "y"
digits = input("Include numbers? (y/n): ").lower() == "y"
symbols = input("Include symbols? (y/n): ").lower() == "y"

characters = ""

if uppercase:
    characters += string.ascii_uppercase
if lowercase:
    characters += string.ascii_lowercase
if digits:
    characters += string.digits
if symbols:
    characters += string.punctuation

if characters == "":
    print("❌ Error: Select at least one character type.")
    exit()

password = "".join(random.choice(characters) for _ in range(length))

print("\n✅ Generated Password:", password)
