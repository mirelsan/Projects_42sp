def input_temperature(temp_str: str) -> int:
    temperature = int(temp_str)
    if temperature > 40:
        raise ValueError(
            f"{temperature}°C is too hot for plants (max 40°C)")
    if temperature < 0:
        raise ValueError(
            f"{temperature}°C is too cold for plants (min 0°C)")
    return temperature


def test_temperature() -> None:
    print("=== Garden Temperature Checker ===\n")

    test_inputs = ['25', 'abc', '100', '-50']

    i = 0
    while i < len(test_inputs):
        data = test_inputs[i]
        print(f"Input data is '{data}'")
        try:
            temperature = input_temperature(data)
            print(f"Temperature is now {temperature}°C\n")
        except ValueError as e:
            print(f"Caught input_temperature error: {e}\n")
        i += 1

    print("All tests completed - program didn't crash!")


def main() -> None:
    test_temperature()


if __name__ == "__main__":
    main()
