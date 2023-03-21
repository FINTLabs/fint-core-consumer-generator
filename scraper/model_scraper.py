from bs4 import BeautifulSoup
from tools.translator import Translator


class ModelScraper:
    def __init__(self):
        self.translator = Translator()

    def scrape(self, component: str):
        component = component.replace("-", ".")
        models = []

        with open('./information_model.html', 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        filtered_divs = [div for div in soup.find_all('div', class_='mat-card-header-text')
                         if div.find('mat-card-subtitle', string=component)]

        for div in filtered_divs:
            if div.h3.small.text == "Hovedklasse":
                models.append(self.translator.translate(div.h3.span.text))

        return models
