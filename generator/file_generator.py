import os


class FileGenerator:
    def __init__(self, ):
        self.file_contents = None

    def read_file(self, file_path: str):
        with open(file_path, "r") as file:
            self.file_contents = file.read()

    def replace_content(self, component_name: str = None, model_name: str = None):
        if component_name:
            domain, package = component_name.split("-")
            self.file_contents = self.file_contents \
                .replace("DOMAIN_CAP", domain.capitalize()) \
                .replace("PACKAGE_CAP", package.capitalize()) \
                .replace("DOMAIN", domain) \
                .replace("PACKAGE", package) \
                .replace("COMPONENT", component_name)

        if model_name:
            self.file_contents = self.file_contents \
                .replace("MODEL_RESOURCES", f"{model_name.capitalize()}Resources") \
                .replace("MODEL_RESOURCE", f"{model_name.capitalize()}Resource") \
                .replace("MODEL_LOWER", model_name.lower()) \
                .replace("MODEL_UPPER", model_name.upper()) \
                .replace("MODEL", model_name.capitalize())

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
