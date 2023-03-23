from generator import FintCoreConsumerGenerator


def main():
    print("Leave blank for latest version")
    version = input("Information model version: ")
    if not version:
        version = "master"

    component = input("fint-core-consumer-")
    consumer_generator = FintCoreConsumerGenerator(component, information_model_version=version)
    consumer_generator.generate_everything()


if __name__ == "__main__":
    main()
