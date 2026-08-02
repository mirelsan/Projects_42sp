def secure_archive(
    filename: str,
    mode: str = "read",
    content: str = "",
) -> tuple[bool, str]:
    if mode == "write":
        try:
            with open(filename, "w") as f:
                f.write(content)
            return True, "Content successfully written to file"
        except OSError as e:
            return False, str(e)
    else:
        try:
            with open(filename) as f:
                return True, f.read()
        except OSError as e:
            return False, str(e)


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print()

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))
    print()

    print("Using 'secure_archive' to read from a regular file:")
    success, data = secure_archive("ancient_fragment.txt")
    print((success, data))
    print()

    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_fragment.txt", "write", data))


if __name__ == "__main__":
    main()
