from scraper import ModelScraper
from generator.file_generator import FileGenerator
from tools import Translator
import os
import shutil


class FintCoreConsumerGenerator:
    def __init__(self, component: str,  information_model_version: str = "master"):
        self.translator = Translator()
        self.model_scraper = ModelScraper()
        self.file_generator = FileGenerator()

        self.component = self.translator.replace(component)
        self.domain, self.package = self.component.split("-")
        self.model_scraper.fetch_models(information_model_version, self.domain, self.package)
        self.models = self.model_scraper.get_main_models()
        self.output_directory = f"./output/fint-core-consumer-{self.domain.lower()}-{self.package.lower()}/"

    def generate_consumer(self):
        self._generate_structure()
        self._generate_base()
        self._generate_model()
        self._generate_rest_endpoint()
        self._generate_link_mapper()
        self._generate_kustomize()
        self._generate_resources()

    def _generate_structure(self):
        source_dir = './input/static/'
        for root, dirs, files in os.walk(source_dir):
            for file_name in files:
                source_path = os.path.join(root, file_name)
                dest_path = os.path.join(self.output_directory, os.path.relpath(source_path, source_dir))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copyfile(source_path, dest_path)

    def _generate_base(self):
        source_dir = './input/base/'
        for file_name in os.listdir(source_dir):
            self.file_generator.read_file(source_dir + file_name)
            self.file_generator.replace_content(self.component)
            self.file_generator.generate_file(file_name, self.output_directory)

    def _generate_model(self):
        source_dir = './input/model/'
        for model in self.models:
            output_dir = self.output_directory + f"src/main/java/no/fintlabs/consumer/model/{model.name.lower()}/"
            os.makedirs(output_dir)
            for file_name in os.listdir(source_dir):
                self.file_generator.read_file(source_dir + file_name)
                self.file_generator.replace_content(self.component, model.name)
                self.file_generator.generate_file(file_name, output_dir, model.name)

    def _generate_rest_endpoint(self):
        source_dir = './input/config/'
        output_dir = self.output_directory + "src/main/java/no/fintlabs/consumer/config/"
        file_name = "RestEndpoints.java"

        with open(source_dir + file_name, "r") as file:
            contents = file.read()

        for model in self.models:
            new_line = f'    public static final String {model.name.upper()} = "/{model.name.lower()}";'
            lines = contents.splitlines()
            for i, line in enumerate(lines):
                if 'public enum RestEndpoints {' in line:
                    lines.insert(i + 4, new_line)
                    break
            contents = '\n'.join(lines)

        with open(output_dir + file_name, 'w') as new_file:
            new_file.write(contents)

    def _generate_link_mapper(self):
        source_dir = './input/config/'
        output_dir = self.output_directory + "src/main/java/no/fintlabs/consumer/config/"
        file_name = "LinkMapper.java"

        with open(source_dir + file_name, "r") as file:
            contents = file.read()

        for model in self.models:
            new_line = f'            .put("no.fint.model.{self.domain}.{self.package}.{model.name.capitalize()}", "/{self.domain}/{self.package}/{model.name.lower()}")'
            lines = contents.splitlines()
            for i, line in enumerate(lines):
                if 'return ImmutableMap.<String,String>builder()' in line:
                    lines.insert(i + 1, new_line)
                    break
            contents = '\n'.join(lines)

        with open(output_dir + file_name, 'w') as new_file:
            new_file.write(contents)

    def _generate_kustomize(self):
        source_dir = './input/kustomize/'
        output_dir = self.output_directory + 'kustomize/'
        for root, dirs, files in os.walk(source_dir):
            for filename in files:
                if not os.path.exists(root.replace(source_dir, output_dir)):
                    os.makedirs(root.replace(source_dir, output_dir))
                path_to_file = root + "/"
                self.file_generator.read_file(path_to_file + filename)
                self.file_generator.replace_content(self.component)
                self.file_generator.generate_file(filename, path_to_file.replace(source_dir, output_dir))

    def _generate_resources(self):
        source_dir = './input/resources/'
        output_dir = self.output_directory + 'src/main/resources/'

        for file in os.listdir(source_dir):
            self.file_generator.read_file(source_dir + file)
            self.file_generator.replace_content()
            self.file_generator.generate_file(file, output_dir)
