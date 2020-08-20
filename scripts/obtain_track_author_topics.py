import argparse
import logging
import pickle

from collections import Counter

import pandas as pd

from common import PMC_FILE_PATH, OUTPUT_FORMATS, load_final_pipe, _write_json_contents


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parseargs():
    parser = argparse.ArgumentParser(description="Obtain author topics for the publications track dataset")
    parser.add_argument('-o', '--output', help="Name of the file where the results will be saved. " +
        "If no output file is specified, results will be written to the console instead.",
        nargs='?', default=None)
    return parser.parse_args()

def show_author_results(pmc_df, articles, topics, output):
    res = {}
    authors_str = pmc_df['authors'].values
    authors_list = [authors.split('|') for authors in authors_str]
    unique_authors = set([a for authors in authors_list for a in authors])
    for author in unique_authors:
        author_topics = []
        for idx, article_topics in enumerate(topics):
            pmc_row = pmc_df.loc[idx]
            article_authors = pmc_row['authors'].split('|')
            if author not in article_authors:
                continue
            author_topics += article_topics
        author_main_topics = Counter(author_topics).most_common(5)
        author_main_topics = [t[0][0] for t in author_main_topics]
        res[author] = {
            'topics': [{
                'labels': t.labels,
                'external_ids': t.uris,
                'descriptions': t.descs
            } for t in author_main_topics]
        }
    _write_json_contents(res, output)


def main(args):
    logger.info('Reading track dataset...')
    pmc_df = pd.read_pickle(PMC_FILE_PATH)
    logger.info('Loading topic extraction model...')
    final_pipe = load_final_pipe()
    articles = pmc_df['text_cleaned'].values
    logger.info('Predicting topics...')
    topics = final_pipe.transform(articles)
    logger.info('Writting results...')
    show_author_results(pmc_df, articles, topics, args.output)

if __name__ == '__main__':
    args = parseargs()
    exit(main(args))
