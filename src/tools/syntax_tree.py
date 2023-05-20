import spacy
from nltk import Tree


class SyntaxTree:
    def __init__(self):
        self.dependency_tree = None
        self.nlp = spacy.load('ru_core_news_sm')

    def to_nltk_tree(self, node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(node, [self.to_nltk_tree(child) for child in node.children])

        return node

    def make_dependency_tree(self, text):
        """
        Makes a dependency tree.
        Args:
          text (str): original text
        """
        doc = self.nlp(text)
        for sent in doc.sents:
            self.dependency_tree = self.to_nltk_tree(sent.root)

        return self.dependency_tree
