from scraper import ModelScraper
from generator.file_generator import FileGenerator
from tools import Translator
import os
import shutil


class FintCoreConsumerGenerator:
    def __init__(self, component: str,  information_model_version: str = "master"):
        self._translator = Translator()
        self._model_scraper = ModelScraper()
        self._file_generator = FileGenerator()

        self._component = self._translator.replace(component)
        self._domain, self.package = self._component.split("-")
        self._model_scraper.fetch_models(information_model_version, self._domain, self.package)
        self._models = self._model_scraper.get_main_models()
        self._base_folder_name = f"fint-core-consumer-{self._domain.lower()}-{self.package.lower()}"
        self.output_directory = f"./output/{self._base_folder_name}/"
        self._model_path = "src/main/java/no/fintlabs/consumer/model/"
        self._config_path = "src/main/java/no/fintlabs/consumer/config/"

    def generate_consumer(self):
        self._generate_structure()
        self._generate_base()
        self._generate_model()
        self._generate_rest_endpoint()
        self._generate_link_mapper()
        self._generate_kustomize()
        self._generate_resources()

    def update_consumer_models(self, path_to_consumer: str, override=False):
        self.output_directory = self._validate_and_set_path(path_to_consumer, self._base_folder_name)
        self._generate_model(override)

    def _delete_existing_models(self):
        existing_model_names = self._get_existing_model_names()

        for folder in existing_model_names:
            full_folder_path = os.path.join(self.output_directory, self._model_path, folder.lower())
            if os.path.exists(full_folder_path):
                shutil.rmtree(full_folder_path)

    def _get_existing_model_names(self):
        full_path = os.path.join(self.output_directory, self._model_path)
        if os.path.exists(full_path):
            return next(os.walk(full_path))[1]
        raise ValueError(f"Path does not exist: {full_path}")

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
            self._file_generator.read_file(source_dir + file_name)
            self._file_generator.replace_content(self._component)
            self._file_generator.generate_file(file_name, self.output_directory)

    def _generate_model(self, override=False):
        if override:
            self._delete_existing_models()

        source_dir = './input/model/'
        for model in self._models:
            output_dir = os.path.join(self.output_directory, self._model_path, model.name.lower())
            os.makedirs(output_dir, exist_ok=True)
            for file_name in os.listdir(source_dir):
                self._file_generator.read_file(source_dir + file_name)
                self._file_generator.replace_content(self._component, model.name)
                self._file_generator.generate_file(file_name, output_dir, model.name)

    def _generate_rest_endpoint(self):
        source_dir = './input/config/'
        output_dir = os.path.join(self.output_directory, self._config_path)
        file_name = "RestEndpoints.java"

        with open(source_dir + file_name, "r") as file:
            contents = file.read()

        for model in self._models:
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
        output_dir = os.path.join(self.output_directory, self._config_path)
        file_name = "LinkMapper.java"

        with open(source_dir + file_name, "r") as file:
            contents = file.read()

        for model in self._models:
            new_line = f'            .put("no.fint.model.{self._domain}.{self.package}.{model.name.capitalize()}", "/{self._domain}/{self.package}/{model.name.lower()}")'
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
                self._file_generator.read_file(path_to_file + filename)
                self._file_generator.replace_content(self._component)
                self._file_generator.generate_file(filename, path_to_file.replace(source_dir, output_dir))

    def _generate_resources(self):
        source_dir = './input/resources/'
        output_dir = self.output_directory + 'src/main/resources/'

        for file in os.listdir(source_dir):
            self._file_generator.read_file(source_dir + file)
            self._file_generator.replace_content()
            self._file_generator.generate_file(file, output_dir)

    @staticmethod
    def _validate_and_set_path(path: str, base_folder: str):
        if os.path.isabs(path):
            if os.path.isdir(path):
                if os.path.basename(path) == base_folder:
                    return path
                elif os.path.basename(f"{path}/{base_folder}") == base_folder:
                    return f"{path}/{base_folder}"
                raise ValueError(f"Invalid absolute path - folder {base_folder} not found")
            raise ValueError("Invalid absolute path - path does not exist or is not a directory")
        else:
            abs_path = os.path.abspath(path)
            if os.path.isdir(abs_path):
                if os.path.basename(abs_path) == base_folder:
                    return abs_path
                elif os.path.basename(f"{path}/{base_folder}") == base_folder:
                    return f"{path}/{base_folder}"
                raise ValueError(f"Invalid relative path - folder {base_folder} not found")
            raise ValueError("Invalid relative path - path does not exist or is not a directory")
