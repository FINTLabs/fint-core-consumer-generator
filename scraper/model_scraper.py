from tools.translator import Translator
from scraper.model import Model
import xml.etree.ElementTree as Et
import urllib.request


XML_BASE_URL = "https://raw.githubusercontent.com/FINTLabs/fint-informasjonsmodell"


class ModelScraper:
    def __init__(self):
        self._translator = Translator()
        self._abstract_trees: list[Et.Element] = []
        self._model_trees: list[Et.Element] = []
        self._common_model_trees: list[Et.Element] = []
        self._connector_trees: list[Et.Element] = []
        self._common_model_checklist = {}
        self.models: list[Model] = []

    def fetch_models(self, version: str, package: str):
        root = self.get_xml_root(version)
        self._update_tree_lists(root, package)
        self._reset_common_model_checklist()
        self._get_connector_tree(root)
        self._update_models_from_trees()

    def _update_tree_lists(self, root, package: str):
        for element in root[2][0]:
            is_class = 'uml:Class' in element.attrib.values()
            if is_class:
                is_abstract = element[1].get('isAbstract') == 'true'
                is_hovedklasse = element[1].get('stereotype') == 'hovedklasse'
                has_package_name = 'package_name' in element[7].attrib.keys()
                if is_abstract:
                    self._abstract_trees.append(element)
                elif has_package_name and is_hovedklasse:
                    package_name = element[7].attrib['package_name']
                    if package_name == package.capitalize():
                        self._model_trees.append(element)
                    elif package_name == "Felles":
                        self._common_model_trees.append(element)

    def _update_models_from_trees(self):
        for element in self._model_trees:
            model = Model(self._translator.replace(element.get('name')))
            model = self._update_model_for_writeable(model, element)

            links = element.find('links')
            if links is not None:
                for link in links:
                    link_id = list(link.attrib.values())[0]
                    for connector_tree in self._connector_trees:
                        connector_id = list(connector_tree.attrib.values())[0]
                        if link_id == connector_id:
                            target_model = connector_tree.find('./target/model')
                            target_model_name = target_model.get('name')
                            self._check_for_common_models(target_model_name)
                            if model.writeable is False:
                                model = self._check_for_abstract_relations(model, target_model_name)
            self.models.append(model)

    def _check_for_abstract_relations(self, model:Model, target_model: str):
        for abstract_element in self._abstract_trees:
            abstract_model_name = abstract_element.get('name')
            if target_model == abstract_model_name:
                model = self._update_model_for_writeable(model, abstract_element)
                return model
        return model

    def _check_for_common_models(self, target_model_name: str):
        for common_element in self._common_model_trees:
            common_model_name = common_element.get('name')
            if target_model_name == common_model_name:
                if not self._common_model_checklist[common_model_name]:
                    self._common_model_checklist[common_model_name] = True
                    common_model = Model(self._translator.replace(common_model_name))
                    common_model.common = True
                    common_model = self._update_model_for_writeable(common_model, common_element)
                    self.models.append(common_model)

    @staticmethod
    def _update_model_for_writeable(model: Model, element: Et.Element):
        attributes = element.find('attributes')
        if attributes is not None:
            for attribute in attributes:
                is_writable = attribute.find('stereotype[@stereotype="writable"]') is not None
                if is_writable:
                    model.writeable = True
                    return model
        return model

    def _get_connector_tree(self, root: Et.Element):
        for i in root[2][1]:
            self._connector_trees.append(i)

    @staticmethod
    def update_model_for_writeable(element: Et.Element, model: Model) -> Model:
        for attribute in element.findall('attribute'):
            is_writeable = attribute.find('stereotype[@stereotype="writable"]') is not None
            if is_writeable:
                model.writeable = True
                return model
        return model

    @staticmethod
    def _get_common_models_dict(common_model_trees):
        common_model_dict = {}
        for common_model_tree in common_model_trees:
            common_model_dict[common_model_tree.attrib['name']] = False
        return common_model_dict

    def get_xml_root(self, version: str):
        """Fetches XML content from the URL and returns its root element."""
        xml_content = self._fetch_xml_content(version)
        return Et.fromstring(xml_content)

    @staticmethod
    def _fetch_xml_content(version: str):
        """Fetches XML content from the URL based on the given version."""
        if version in ["master", "main"]:
            url = f"{XML_BASE_URL}/{version}/FINT-informasjonsmodell.xml"
        else:
            url = f"{XML_BASE_URL}/v{version}/FINT-informasjonsmodell.xml"
        response = urllib.request.urlopen(url)
        if response.status == 200:
            return response.read().decode('windows-1252', 'replace')
        else:
            raise ValueError(f"Invalid version: {version} got status code: {response.status}")

    def _reset_common_model_checklist(self):
        for element in self._common_model_trees:
            self._common_model_checklist[element.get('name')] = False
