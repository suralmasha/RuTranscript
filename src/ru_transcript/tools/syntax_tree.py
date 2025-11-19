import spacy
from nltk import Tree
from spacy.tokens import Token


class SyntaxTree:
    """SyntaxTree with an NLP model and empty dependency tree."""

    def __init__(self) -> None:
        """Initialize SyntaxTree."""
        self.dependency_tree = None
        self.nlp = spacy.load('ru_core_news_sm')

    def to_nltk_tree(self, node: Token) -> Tree | Token:
        """
        Convert a spaCy dependency node into an NLTK Tree recursively.

        param node: spaCy token node.
        return: NLTK Tree or spaCy token if it is a leaf.
        """
        if node.n_lefts + node.n_rights > 0:
            return Tree(node, [self.to_nltk_tree(child) for child in node.children])

        return node

    def make_dependency_tree(self, text: str) -> Tree:
        """
        Make a dependency tree for the input text.

        param text: Original text.
        return: NLTK Tree representing the dependency tree.
        """
        doc = self.nlp(text)
        for sent in doc.sents:
            self.dependency_tree = self.to_nltk_tree(sent.root)

        return self.dependency_tree
