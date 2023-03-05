print("Attempt # 1\n")

try:
    for name in globals():
        print(name)
except RuntimeError as e:
    print(f"error: {str(e)}")

print("\n\nAttempt #2\n")


name = None
for name in globals():
    print(name)
