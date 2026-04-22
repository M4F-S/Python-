def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    for sample in ("25", "abc"):
        print(f"Input data is '{sample}'")
        try:
            temp = input_temperature(sample)
            print(f"Temperature is now {temp}°C")
        except Exception as e:
            print(f"Caught input_temperature error: {e}")
        print()


if __name__ == "__main__":
    print("=== Garden Temperature ===")
    print()
    test_temperature()
    print("All tests completed - program didn't crash!")
