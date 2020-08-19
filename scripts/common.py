import csv
import joblib
import json
import os
import sys

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

from herc_common.utils import add_text_topics_to_graph, load_object, EDMA, ITSRDF, NIF

RESULTS_DIR = 'results'
NOTEBOOK_2_RESULTS_DIR = os.path.join(RESULTS_DIR, '2_data_exploration')
NOTEBOOK_7_RESULTS_DIR = os.path.join(RESULTS_DIR, '7_complete_system')

PMC_DF_FILE_PATH = os.path.join(NOTEBOOK_2_RESULTS_DIR, 'pmc_dataframe.pkl')
FINAL_PIPE_FILE_PATH = os.path.join(NOTEBOOK_7_RESULTS_DIR, 'final_pipe.pkl')

RDF_FORMATS = {'json-ld', 'n3', 'xml', 'turtle'}
OUTPUT_FORMATS = RDF_FORMATS | {'csv', 'json'}

def create_pmc_graph(pmc_df, articles, topics):
    g = Graph()
    g.bind('edma', EDMA)
    g.bind('itsrdf', ITSRDF)
    g.bind('nif', NIF)
    collection_element = URIRef(f"{EDMA}{joblib.hash(pmc_df)}")
    g.add((collection_element, RDF.type, NIF.ContextCollection))
    for idx, article_topics in enumerate(topics):
        text = articles[idx]
        pmc_row = pmc_df.loc[idx]
        uri = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{article_id}/fullTextXML"
        pmc_id = pmc_row['id']
        context_element = add_text_topics_to_graph(uri, gh_id, text, article_topics, g)
        g.add((collection_element, NIF.hasContext, context_element))
    return g

def load_final_pipe():
    import string
    import en_core_sci_lg
    from collections import Counter
    from tqdm import tqdm

    en_core_sci_lg.load()
    return load_object(FINAL_PIPE_FILE_PATH)

def show_pmc_csv_results(pmc_df, articles, topics, out_file):
    fieldnames = ['article_id', 'topics']
    if out_file is not None:
        with open(out_file, 'w', encoding='utf-8') as f:
            csvwriter = csv.DictWriter(f, fieldnames=fieldnames)
            _write_csv_contents(csvwriter, pmc_df, articles, topics)
    else:
        csvwriter = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        _write_csv_contents(csvwriter, pmc_df, articles, topics)

def show_pmc_graph_results(pmc_df, articles, topics, format, out_file):
    g = create_pmc_graph(pmc_df, articles, topics)
    if out_file is not None:
        g.serialize(destination=out_file, format=format)
    else:
        print(g.serialize(format=format).decode("utf-8"))

def show_pmc_json_results(pmc_df, articles, topics, out_file):
    res = {}
    for idx, article_topics in enumerate(topics):
        article_topics = [t[0] for t in article_topics]
        article_row = pmc_df.loc[idx]
        article_id = article_row['id']
        article_title = article_row['title']
        article_authors = article_row['authors'].split('|')
        source_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{article_id}/fullTextXML"
        res[str(article_id)] = {
            'source_url': source_url,
            'authors': article_authors,
            'title': article_title,
            'topics': [{
                'labels': t.labels,
                'external_ids': t.uris,
                'descriptions': t.descs,
                'score': t.score
            } for t in article_topics]
        }
    _write_json_contents(res, out_file)

def show_results(pmc_df, articles, topics, out_file, format):
    if format in RDF_FORMATS:
        show_pmc_graph_results(pmc_df, articles, topics, format, out_file)
    elif format == 'csv':
        show_pmc_csv_results(pmc_df, articles, topics, out_file)
    else:
        show_pmc_json_results(pmc_df, articles, topics, out_file)


def _write_csv_contents(csvwriter, pmc_df, articles, topics):
    csvwriter.writeheader()
    for idx, article_topics in enumerate(topics):
        article_topics = [t[0] for t in article_topics]
        article_id = pmc_df.loc[idx]['id']
        csvwriter.writerow({
            'article_id': article_id,
            'topics': ' - '.join([str(t) for t in article_topics])
        })

def _write_json_contents(res, out_file):
    if out_file is not None:
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))
