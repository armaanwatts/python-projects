import re

print("=== Password Strength Checker ===")

password = input("Enter password: ")

score = 0

# Length checks
if len(password) >= 8:
    score += 1
if len(password) >= 12:
    score += 1

# Character checks
if re.search(r"[A-Z]", password):
    score += 1
if re.search(r"[a-z]", password):
    score += 1
if re.search(r"[0-9]", password):
    score += 1
if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
    score += 1

print("\n--- Password Report ---")
print("Length:", len(password))

if score <= 2:
    print("Strength: WEAK ❌")
elif score <= 4:
    print("Strength: MEDIUM ⚠️")
else:
    print("Strength: STRONG ✅")

print("\nTip: Use at least 12 characters with uppercase, lowercase, numbers, and symbols.")
