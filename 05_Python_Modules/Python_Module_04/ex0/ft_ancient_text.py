import sys


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return

    filename = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Acessing file '{filename}'")

    try:
        f = open(filename)
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return

    content = f.read()
    print("---\n")
    print(content)
    print("---")

    f.close()
    print(f"File '{filename}' closed.")


if __name__ == "__main__":
    main()
