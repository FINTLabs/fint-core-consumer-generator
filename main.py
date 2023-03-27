from generator import FintCoreConsumerGenerator


def main():
    component = input("fint-core-consumer-")
    print("Leave blank for latest version")
    version = input("Information model version: ")
    if not version:
        version = "master"

    consumer_generator = FintCoreConsumerGenerator(component, version)
    override = input("Override Y/N: ")
    if override.lower() in ("y", "ye", "yes", "yea"):
        consumer_generator.generate_consumer(override=True)
    else:
        consumer_generator.generate_consumer()


if __name__ == "__main__":
    main()
