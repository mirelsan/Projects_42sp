def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        "abc" + 123  # type: ignore[operator]
    else:
        print("Operation completed successfully")
        print()


def test_error_types() -> None:
    i = 0
    while i < 5:
        print(f"Testing operation {i}...")
        try:
            garden_operations(i)
        except (
            ValueError,
            ZeroDivisionError,
            FileNotFoundError,
            TypeError,
        ) as e:
            print(f"Caught {type(e).__name__}: {e}")
        i += 1

    print("All error types tested successfully")


def main() -> None:
    print("=== Garden Error Types Demo ===\n")
    test_error_types()


if __name__ == "__main__":
    main()
