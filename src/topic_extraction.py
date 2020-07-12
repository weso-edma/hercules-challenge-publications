from joblib import Parallel, delayed
import multiprocessing.dummy as mp
import networkx.algorithms as nxa

from sklearn.base import TransformerMixin, BaseEstimator
from tqdm.notebook import tqdm

from .graph import get_centrality_algorithm_results, get_largest_connected_subgraph


class TopicLabeller(BaseEstimator, TransformerMixin):
    def __init__(self, graph_builder,
                 r=nxa.centrality.information_centrality,
                 num_labels_per_topic=1,
                 stop_uris=None):
        self.graph_builder = graph_builder
        self.r = r
        self.num_labels = num_labels_per_topic
        self.stop_uris = [] if stop_uris is None else stop_uris
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, *args, **kwargs):
        pool = mp.Pool()
        results = pool.map(self.get_topic_labels, X)
        #results = Parallel(n_jobs=20)(delayed(self.get_topic_labels)(linked_entities) for linked_entities in X)
        return results
        #return [self.get_topic_labels(topic) for topic in tqdm(X)]
    
    def get_topic_labels(self, linked_entities):
        topic_neighbourhood = self.graph_builder.build_graph(linked_entities)
        subgraph = get_largest_connected_subgraph(topic_neighbourhood)
        return get_centrality_algorithm_results(subgraph, self.r,
            self.stop_uris, self.num_labels)
