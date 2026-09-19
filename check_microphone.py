import sounddevice as sd


def main():
    print("Available audio devices:")
    print(sd.query_devices())

    print("\nDefault input device:")
    try:
        default_input = sd.query_devices(kind="input")
        print(default_input)
    except Exception as error:
        print(f"Unable to find a default microphone: {error}")


if __name__ == "__main__":
    main()
