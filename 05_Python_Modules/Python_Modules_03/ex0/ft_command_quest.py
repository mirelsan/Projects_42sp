import sys

print("=== Command Quest ===")
print(f"Program name: {sys.argv[0]}")
if len(sys.argv) < 2:
    print("No arguments provided!")
    print(f"Total arguments: {len(sys.argv)}")
else:
    arg = sys.argv[1:]
    print(f"Arguments received: {len(arg)}")
    count = 1
    for argument in arg:
        print(f"Argument {count}: {argument}")
        count += 1
    print(f"Total arguments: {len(sys.argv)}")
