from generator import FintCoreConsumerGenerator


def main():
    print("Can be left blank")
    version = input("Information model version: ")
    if not version:
        version = "3.13.10"

    component = input("fint-core-consumer-")
    consumer_generator = FintCoreConsumerGenerator(component, information_model_version=version)
    consumer_generator.generate_everything()


if __name__ == "__main__":
    main()
