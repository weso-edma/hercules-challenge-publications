import json
import requests

from src.utils import WIKIDATA_BASE

class WikidataEntityLinker():
    def fit(self, X, y, *args):
        return self
    
    def transform(self, X, y, *args):
        return [self.link_entity(entity) 
                for doc in X
                for entity in doc]
    
    def link_entity(self, entity_label):
        url = f"{WIKIDATA_BASE}/api.php?action=wbsearchentities&search=" + \
            f"{entity_label}&language=en&format=json"
        response = requests.get(url)
        if response.status_code != 200:
            raise Error()
        content = json.loads(response.text)
        search_results = content['search']
        if len(search_results) == 0:
            return (entity_label, None)
        return (entity_label, search_results[0]['concepturi'])

