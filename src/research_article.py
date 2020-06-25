class ResearchArticle():
    def __init__(self, article_id, title, authors, abstract,
                 full_body, references_titles, subjects=None):
        self.article_id = article_id
        self.authors = authors
        self.abstract = abstract
        self.full_body = full_body
        self.title = title
        self.references_titles = references_titles
        self.subjects = subjects if subjects is not None else []
    
    def to_dict(self):
        return {
            'id': self.article_id,
            'title': self.title,
            'abstract': self.abstract,
            'full_body': self.full_body,
            'authors': '|'.join(self.authors),
            'references': '|'.join(self.references_titles),
            'subjects': '|'.join(self.subjects)
        }
    
    def __eq__(self, other):
        if other is None or not isinstance(other, ResearchArticle):
            return False
        return self.article_id == other.article_id
        
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f"{self.article_id} - {self.title} - {self.abstract[:10]}... - {self.full_body[:20]}..."
