import os
from scraper import Model


class FileGenerator:
    def __init__(self, ):
        self.file_contents = None

    def read_file(self, file_path: str):
        with open(file_path, "r") as file:
            self.file_contents = file.read()

    def replace_content(self, component_name: str = None, model: Model = None):
        if model:
            self.file_contents = self.file_contents \
                .replace("MODEL_RESOURCES", f"{model.name.capitalize()}Resources") \
                .replace("MODEL_RESOURCE", f"{model.name.capitalize()}Resource") \
                .replace("MODEL_LOWER", model.name.lower()) \
                .replace("MODEL_UPPER", model.name.upper()) \
                .replace("MODEL", model.name.capitalize())
            if model.common:
                self.file_contents = self.file_contents \
                    .replace("DOMAIN.", "felles") \
                    .replace("PACKAGE", "")

        if component_name and not model or component_name and model and model.common is False:
            domain, package = component_name.split("-")
            self.file_contents = self.file_contents \
                .replace("DOMAIN_CAP", domain.capitalize()) \
                .replace("PACKAGE_CAP", package.capitalize()) \
                .replace("DOMAIN", domain) \
                .replace("PACKAGE", package) \
                .replace("COMPONENT", component_name)

    def generate_file(self, file_name: str, output_directory: str, model_name: str = None, override=False):
        if model_name:
            file_name = f"{model_name.capitalize()}{file_name.capitalize()}"

        output_file_path = os.path.join(output_directory, file_name)
        if os.path.exists(output_file_path):
            if override:
                os.remove(output_file_path)
            else:
                return Warning(f"File already exists: {file_name} Consider using override")

        with open(output_file_path, "w") as output_file:
            output_file.write(self.file_contents)
