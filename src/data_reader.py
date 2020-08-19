from bs4 import BeautifulSoup

from . import ResearchArticle

def get_abstract(article_soup):
    return article_soup.find('abstract').text

def get_authors(article_soup):
    return [author.find('name').get_text(separator=' ')
            for author in article_soup.find_all('contrib',
                                        {'contrib-type': 'author'})]

def get_full_body(article_soup):
    return article_soup.find('body').get_text(separator=' ')

def get_title(article_soup):
    return article_soup.find('article-title').text

def get_references_titles(article_soup):
    return [reference.find('article-title').text
            for reference in article_soup.find_all('ref')
            if reference.find('article-title')]

def get_subjects(article_soup):
    return [subj.text
            for subj in article_soup.find_all('subject')
            if subj.text.lower() not in ['review', 'article', 'research article']]

def parse_pmc_article(pmc_id, article_xml):
    soup = BeautifulSoup(article_xml, 'lxml-xml')
    return ResearchArticle(pmc_id, get_title(soup),
                           get_authors(soup), get_abstract(soup),
                           get_full_body(soup), get_references_titles(soup),
                           get_subjects(soup))
