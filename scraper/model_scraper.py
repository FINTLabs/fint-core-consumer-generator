from tools.translator import Translator
from scraper.model import Model
import xml.etree.ElementTree as Et
import requests


class ModelScraper:
    def __init__(self):
        self.translator = Translator()
        self.models = list()

    def get_main_models(self):
        return [model for model in self.models if not model.deprecated]

    def get_deprecated_models(self):
        return [model for model in self.models if model.deprecated]

    def fetch_models(self, version: str, domain: str, package: str):
        root = self.__get_xml_root(version)
        valid_ids = self._get_valid_ids(root)
        domain = self._get_domain(root, domain)
        package = self._get_package(domain, package)
        models = self._get_models_from_package(package)
        self._update_models(models, valid_ids)

    @staticmethod
    def _get_package(domain, input_package: str):
        for package in domain:
            if "name" in package.attrib.keys():
                if input_package.capitalize() in package.attrib["name"]:
                    return package
        raise ValueError(f"Package not found: {input_package}")

    @staticmethod
    def _get_domain(root, input_domain: str):
        for domain in root[1][0][0]:
            if input_domain.capitalize() in domain.attrib["name"]:
                return domain
            continue
        raise ValueError(f"Domain not found: {input_domain}")

    @staticmethod
    def _get_valid_ids(root):
        main_ids = set()
        for model in root[1]:
            if "hovedklasse" in model.tag:
                main_ids.add(model.attrib["base_Class"])
        return main_ids

    def __get_xml_root(self, version: str):
        xml_content = self.__get_xml_content(version)
        return Et.fromstring(xml_content)

    @staticmethod
    def __get_xml_content(version: str):
        if version in ["master", "main"]:
            url = f"https://raw.githubusercontent.com/FINTLabs/fint-informasjonsmodell/{version}/FINT-informasjonsmodell.xml"
        else:
            url = f"https://raw.githubusercontent.com/FINTLabs/fint-informasjonsmodell/v{version}/FINT-informasjonsmodell.xml"
        response = requests.get(url)
        if response.status_code == 200:
            return response.content.decode('windows-1252', 'replace')
        else:
            raise ValueError(f"Invalid version: {version} got status code: {response.status_code}")

    @staticmethod
    def _get_models_from_package(package):
        model_list = []
        for model in package:
            if "uml:Class" in model.attrib.values() and "isAbstract" not in model.attrib.keys():
                # list(model.attrib.values())[1] == id (needs to be done for backwards and forwards compatibility)
                model = Model(model.attrib["name"], list(model.attrib.values())[1])
                model_list.append(model)
        if len(model_list) > 0:
            return model_list
        else:
            raise ValueError(f"Could not find any models under package: {package}")

    def _update_models(self, models: list[Model], valid_ids: set[str]):
        for model in models:
            if model.id not in valid_ids:
                model.deprecated = True
            model.name = self.translator.replace(model.name)
            self.models.append(model)
