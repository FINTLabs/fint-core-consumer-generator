from generator import FintCoreConsumerGenerator


def main():
    component = input("fint-core-consumer-")
    create_or_update = input("Create or Update: ")
    print("Leave blank for latest version")
    version = input("Information model version: ")
    if not version:
        version = "master"

    consumer_generator = FintCoreConsumerGenerator(component, version)

    if create_or_update.lower() in ("c", "cr", "cre", "crea", "creat", "create"):
        return consumer_generator.generate_consumer()

    path_to_consumer = input("Path: ")
    override = input("Override Y/N: ")
    if override.lower() in ("y", "ye", "yes"):
        consumer_generator.update_consumer_models(path_to_consumer, override=True)
    else:
        consumer_generator.update_consumer_models(path_to_consumer)


if __name__ == "__main__":
    main()
