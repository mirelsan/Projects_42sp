import sys


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return

    filename = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Acessing file '{filename}'")

    try:
        f = open(filename)
    except OSError as e:
        print(f"[STDERR] Error opening file '{filename}': {e}",
              file=sys.stderr)
        return

    content = f.read()
    print("---\n")
    print(content)
    print("---")
    f.close()
    print(f"File '{filename}' closed.")

    lines = content.splitlines()
    transformed_lines = [line + "#" for line in lines]
    transformed = "\n".join(transformed_lines)

    print("Transform data:")
    print("---\n")
    print(transformed)
    print("---")

    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    new_filename = sys.stdin.readline().rstrip("\n")

    if new_filename == "":
        print("Not saving data.")
        return

    print(f"Saving data to '{new_filename}'")
    try:
        out = open(new_filename, "w")
    except OSError as e:
        print(f"[STDERR] Error opening file '{new_filename}': {e}",
              file=sys.stderr,)
        print("Data not saved.")
        return

    out.write(transformed)
    out.close()
    print(f"Data saved in file '{new_filename}'.")


if __name__ == "__main__":
    main()
