import json
import networkx as nx
import networkx.algorithms as nxa
import requests

from bokeh.io import output_file
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool,)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx

from .utils import empty_if_keyerror, WIKIDATA_BASE


WIKIDATA_PROPS_EXPAND = ['P31', 'P279', 'P301', 'P361', 'P366',
                         'P527', 'P910', 'P921', 'P2578', 'P2579']


def build_graph_plot(G, title=""):
    plot = Plot(plot_width=400, plot_height=400,
                x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = title
    
    node_attrs = {}
    for node in G.nodes(data=True):
        node_color = Spectral4[node[1]['n']]
        node_attrs[node[0]] = node_color
    nx.set_node_attributes(G, node_attrs, "node_color")

    node_hover_tool = HoverTool(tooltips=[("Label", "@label"), ("n", "@n")])
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color="node_color")
    graph_renderer.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width=1)
    plot.renderers.append(graph_renderer)
    return plot


def get_centrality_algorithm_results(g, algorithm, stop_uris, top_n):
        metrics = algorithm(g)
        metrics = {key: val for key, val in metrics.items()
                   if g.nodes[key]['n'] != 0
                   and key not in stop_uris}
        best_qids = sorted(metrics, key=metrics.get, reverse=True)[:top_n]
        return [(g.nodes[qid]['label'], metrics[qid]) for qid in best_qids]


def get_largest_connected_subgraph(g):
    """
    """
    S = [g.subgraph(c).copy() for c in nxa.components.connected_components(g)]
    return max(S, key=len)

def _build_uri(entity_id):
    return f"http://www.wikidata.org/entity/{entity_id}"

@empty_if_keyerror
def _get_aliases(entity_info, lang='en'):
    return [alias['value'] 
            for alias in entity_info['aliases'][lang]]


@empty_if_keyerror
def _get_desc(entity_info, lang='en'):
    return entity_info['descriptions'][lang]['value']

@empty_if_keyerror
def _get_labels(entity_info, lang='en'):
    return entity_info['labels'][lang]['value']


class WikidataGraphBuilder():
    def __init__(self, max_hops=2, additional_props=None):
        self.max_hops = max_hops
        self.props_to_expand = WIKIDATA_PROPS_EXPAND
        if additional_props:
            self.props_to_expand += additional_props
    
    def build_graph(self, topic):
        G = nx.Graph()
        for term in topic:
            term_uri = term[1]
            if term_uri is not None:
                term_id = term_uri.split('/')[-1]
                self._add_wd_node_info(G, term_id, None, 0)
        return G
    
    def _add_wd_node_info(self, graph, term_id, prev_node, curr_hop):
        print(f"Visiting entity '{term_id}' - Curr hop: {curr_hop}")
        if curr_hop > self.max_hops or term_id == 'Q4167836':
            return
        
        # call wikidata API for uri
        endpoint = f"{WIKIDATA_BASE}/api.php?action=wbgetentities&ids={term_id}&languages=en&format=json"
        res = requests.get(endpoint)
        if res.status_code != 200:
            raise Error()
        
        content = json.loads(res.text)
        entity_info = content['entities'][term_id]
        
        if term_id not in graph.nodes:
            graph.add_node(term_id)
            #graph.nodes[term_id]['alias'] = _get_aliases(entity_info)
            graph.nodes[term_id]['desc'] = _get_desc(entity_info)
            graph.nodes[term_id]['label'] = _get_labels(entity_info)
            graph.nodes[term_id]['n'] = curr_hop

        if prev_node is not None and not graph.has_edge(prev_node, term_id):
            graph.add_edge(prev_node, term_id)
        
        for claim_key, claim_values in entity_info['claims'].items():
            if claim_key not in self.props_to_expand:
                continue
            
            for value in claim_values:
                snaktype = value['mainsnak']['snaktype']
                if snaktype in ['novalue', 'somevalue']:
                    continue
                
                new_node_id = value['mainsnak']['datavalue']['value']['id']
                self._add_wd_node_info(graph, new_node_id, term_id, curr_hop + 1)
