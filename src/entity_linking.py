import json
import requests

from sklearn.base import TransformerMixin, BaseEstimator
from tqdm.notebook import tqdm

from src.utils import WIKIDATA_BASE


class WikidataEntityLinker(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.linked_entities_cache = {}

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, *args, **kwargs):
        return [[self.link_entity(entity) for entity in doc]
                for doc in tqdm(X)]
    
    def link_entity(self, entity_label):
        if entity_label in self.linked_entities_cache:
            return (entity_label, self.linked_entities_cache[entity_label])

        url = f"{WIKIDATA_BASE}/api.php?action=wbsearchentities&search=" + \
            f"{entity_label}&language=en&format=json"
        response = requests.get(url)
        if response.status_code != 200:
            raise Error()
        content = json.loads(response.text)
        search_results = content['search']
        if len(search_results) == 0:
            self.linked_entities_cache[entity_label] = None
            return self.link_entity(entity_label)
        
        self.linked_entities_cache[entity_label] = search_results[0]['concepturi']
        return self.link_entity(entity_label)
