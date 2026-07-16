def input_temperature(temp_str):
    temperature = int(temp_str)
    return temperature


def main():
    print("=== Garden Temperature ===\n")

    test_inputs = ['25', 'abc']

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


if __name__ == "__main__":
    main()