class FileGenerator:
    def __init__(self, component: str):
        self.component = component
        self.domain = self.component.split("-")[0]
        self.package = self.component.split("-")[1]
        self.file_content = None

    def read_file(self, path_to_file: str):
        with open(path_to_file, "r") as file:
            self.file_content = file.read()

    def replace_content(self, model: str = None):
        if not isinstance(self.file_content, str):
            return
        content = self.file_content
        content = content.replace("DOMAIN_CAP", self.domain.capitalize())
        content = content.replace("PACKAGE_CAP", self.package.capitalize())
        content = content.replace("DOMAIN", self.domain)
        content = content.replace("PACKAGE", self.package)
        content = content.replace("COMPONENT", self.component)
        if model:
            content = content.replace("MODEL_RESOURCES", model.capitalize() + "Resources")
            content = content.replace("MODEL_RESOURCE", model.capitalize() + "Resource")
            content = content.replace("MODEL_LOWER", model.lower())
            content = content.replace("MODEL_UPPER", model.upper())
            content = content.replace("MODEL", model.capitalize())

        self.file_content = content

    def generate_file(self, file: str, output_path: str, model: str = None):
        if model:
            file_name = model.capitalize() + file
        else:
            file_name = file
        with open(f"{output_path}{file_name}", "w") as output_file:
            output_file.writelines(self.file_content)
