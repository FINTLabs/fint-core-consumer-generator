from generator import FintCoreConsumerGenerator
from scraper import update_information_model


def main():
    update_info_model = input("Update information model? Y/N: ")
    if update_info_model.lower() in ["yes", "ye", "y"]:
        update_information_model()

    consumer_generator = FintCoreConsumerGenerator()
    consumer_generator.generate_everything()


if __name__ == "__main__":
    main()
