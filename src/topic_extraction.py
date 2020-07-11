from .graph import get_centrality_algorithm_resuts, get_largest_connected_subgraph

class TopicLabeller():
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
    
    def transform(self, X, y=None, **kwargs):
        return [self.get_topics_labels(topic) for topic in X]
    
    def get_topic_labels(self, topic_graph):
        topic_neighbourhood = self.graph_builder.build_graph(topic)
        subgraph = get_largest_connected_subgraph(topic_neighbourhood)
        return get_centrality_algorithm_results(subgraph, self.r,
            self.stop_uris, self.num_labels_per_topic)
