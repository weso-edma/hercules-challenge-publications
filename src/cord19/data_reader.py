import json

from .. import ResearchArticle


def parse_cord_file(file_name):
    try:
        with open(file_name, 'r') as f:
            json_data = json.load(f)
            res = ResearchArticle(parse_id(json_data), parse_title(json_data),
                                  parse_authors(json_data), parse_abstract(json_data),
                                  parse_full_body(json_data), parse_refs(json_data))
    except Exception:
        print(file_name)
    return res

def parse_abstract(json_data):
    try:
        return '\n '.join([abst['text'] for abst in json_data['abstract']])
    except KeyError:
        return "" # no abstract

def parse_authors(json_data):
    return [f"{author['first']} {' '.join(author['middle'])} {author['last']}" 
            for author in json_data['metadata']['authors']]

def parse_full_body(json_data):
    return '\n '.join([bt['text'] for bt in json_data['body_text']])

def parse_id(json_data):
    return json_data['paper_id']

def parse_refs(json_data):
    return [json_data['bib_entries'][bib_key]['title']
            for bib_key in json_data['bib_entries'].keys()]

def parse_title(json_data):
    return json_data['metadata']['title']
