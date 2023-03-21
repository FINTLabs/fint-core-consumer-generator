from scraper import ModelScraper
from generator.file_generator import FileGenerator
import os
import shutil


class FintCoreConsumerGenerator:
    def __init__(self, output_path: str = None):
        self.component = input("fint-core-consumer-")
        self.domain = self.component.split("-")[0]
        self.package = self.component.split("-")[1]
        self.model_scraper = ModelScraper()
        self.file_generator = FileGenerator(self.component)
        self.models = self.model_scraper.scrape(self.component)
        if not output_path:
            self.output_path = f"./output/fint-core-consumer-{self.component}/"
        else:
            self.output_path = output_path

    def generate_everything(self):
        self.generate_structure()
        self.generate_base_files()
        self.generate_model_files()
        self.generate_rest_endpoint_file()
        self.generate_link_mapper()
        self.generate_kustomize_files()
        self.generate_resources()

    def generate_structure(self):
        source_dir = './input/static/'
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_path = os.path.join(root, file)
                dest_path = os.path.join(self.output_path, os.path.relpath(source_path, source_dir))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copyfile(source_path, dest_path)

    def generate_base_files(self):
        source_dir = './input/base/'
        for file in os.listdir(source_dir):
            self.file_generator.read_file(source_dir + file)
            self.file_generator.replace_content()
            self.file_generator.generate_file(file, self.output_path)

    def generate_model_files(self):
        source_dir = './input/model/'
        for model in self.models:
            output_dir = self.output_path + f"src/main/java/no/fintlabs/consumer/model/{model.lower()}/"
            os.makedirs(output_dir)
            for file in os.listdir(source_dir):
                self.file_generator.read_file(source_dir + file)
                self.file_generator.replace_content(model=model)
                self.file_generator.generate_file(file, output_dir, model=model)

    def generate_rest_endpoint_file(self):
        source_dir = './input/config/'
        output_dir = self.output_path + "src/main/java/no/fintlabs/consumer/config/"
        file_name = "RestEndpoints.java"

        with open(source_dir + file_name, "r") as file:
            contents = file.read()

        for model in self.models:
            new_line = f'    public static final String {model.upper()} = "/{model.lower()}";'
            lines = contents.splitlines()
            for i, line in enumerate(lines):
                if 'public enum RestEndpoints {' in line:
                    lines.insert(i + 4, new_line)
                    break
            contents = '\n'.join(lines)

        with open(output_dir + file_name, 'w') as new_file:
            new_file.write(contents)

    def generate_link_mapper(self):
        source_dir = './input/config/'
        output_dir = self.output_path + "src/main/java/no/fintlabs/consumer/config/"
        file_name = "LinkMapper.java"

        with open(source_dir + file_name, "r") as file:
            contents = file.read()

        for model in self.models:
            new_line = f'            .put("no.fint.model.{self.domain}.{self.package}.{model.capitalize()}", "/{self.domain}/{self.package}/{model.lower()}")'
            lines = contents.splitlines()
            for i, line in enumerate(lines):
                if 'return ImmutableMap.<String,String>builder()' in line:
                    lines.insert(i + 1, new_line)
                    break
            contents = '\n'.join(lines)

        with open(output_dir + file_name, 'w') as new_file:
            new_file.write(contents)

    def generate_kustomize_files(self):
        source_dir = './input/kustomize/'
        output_dir = self.output_path + 'kustomize/'
        for root, dirs, files in os.walk(source_dir):
            for filename in files:
                if not os.path.exists(root.replace(source_dir, output_dir)):
                    os.makedirs(root.replace(source_dir, output_dir))
                path_to_file = root + "/"
                self.file_generator.read_file(path_to_file + filename)
                self.file_generator.replace_content()
                self.file_generator.generate_file(filename, path_to_file.replace(source_dir, output_dir))

    def generate_resources(self):
        source_dir = './input/resources/'
        output_dir = self.output_path + 'src/main/resources/'

        for file in os.listdir(source_dir):
            self.file_generator.read_file(source_dir + file)
            self.file_generator.replace_content()
            self.file_generator.generate_file(file, output_dir)