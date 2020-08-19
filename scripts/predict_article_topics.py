import argparse
import logging
import pickle
import os
import re
import sys

import pandas as pd

from common import PMC_FILE_PATH, OUTPUT_FORMATS, load_final_pipe, show_results

parentdir = os.path.dirname('..')
sys.path.insert(0,parentdir)
from src import parse_pmc_article

BMC_BASE_API = 'https://www.ebi.ac.uk/europepmc/webservices/rest'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean(text):
    text = text.replace(u'\u200a', ' ')
    return re.sub(' +', ' ', text).strip()

def load_articles_df(input, is_file, token):
    if is_file:
        with open(input, 'r', encoding='utf-8') as f:
            articles_ids = [line.rstrip('\n') for line in f]
    else:
        articles_ids = [input]
    pmc_data_xml = {pmc_id: requests.get(f"{BMC_BASE_API}/{pmc_id}/fullTextXML").content
                    for pmc_id in articles_ids}
    pmc_articles = [parse_pmc_article(article_id, article_xml)
                    for article_id, article_xml in pmc_data_xml.items()]
    df = pd.DataFrame.from_records([article.to_dict() for article in pmc_articles])
    df['text_cleaned'] = df['full_body'].apply(lambda x: clean(x))
    return df

def parseargs():
    parser = argparse.ArgumentParser(description="Run predictions for the publication track dataset")
    parser.add_argument('input', type=str, help="ID of the PMC article to extract " +
        "the topics from (e.g. PMC3310815). If the --file flag is set, file with the ids of the publications")
    parser.add_argument('--isFile', action='store_true', default=False, help="If present, this flag " +
        "indicates that the input passed to the script is a file with the ids of each publication " +
        "delimited by newlines.")
    parser.add_argument('-f', '--format', choices=OUTPUT_FORMATS, help="Output format of the results. " +
        "If no output format is specified, results are returned in JSON by default.",
        nargs='?', default='json')
    parser.add_argument('-o', '--output', help="Name of the file where the results will be saved. " +
        "If no output file is specified, results will be written to the console instead.",
        nargs='?', default=None)
    return parser.parse_args()

def main(args):
    logger.info('Loading article data...')
    pmc_df = load_articles_df(args.input, args.isFile, args.token)
    logger.info('Loading topic extraction model...')
    final_pipe = load_final_pipe()
    articles = pmc_df['text_cleaned'].values
    logger.info('Predicting topics...')
    topics = final_pipe.transform(articles)
    logger.info('Writting results...')
    show_results(pmc_df, articles, topics, args.output, args.format)

if __name__ == '__main__':
    args = parseargs()
    exit(main(args))
