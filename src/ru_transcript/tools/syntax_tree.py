from __future__ import annotations

from typing import TYPE_CHECKING

from nltk import Tree

from ru_transcript.exceptions import EmptySyntaxTreeError

from .nlp import get_nlp

if TYPE_CHECKING:
    from spacy.tokens import Token


class SyntaxTree:
    """Build NLTK-compatible dependency trees with the shared spaCy model."""

    def to_nltk_tree(self, node: Token) -> Tree | Token:
        """
        Convert a spaCy dependency node into an NLTK Tree recursively.

        param node: spaCy token node.
        return: NLTK Tree or spaCy token if it is a leaf.
        """
        if node.n_lefts + node.n_rights > 0:
            return Tree(node, [self.to_nltk_tree(child) for child in node.children])

        return node

    def make_dependency_tree(self, text: str) -> Tree | Token:
        """
        Make a dependency tree for the input text.

        param text: Original text.
        return: NLTK Tree representing the dependency tree.
        """
        dependency_tree: Tree | Token | None = None
        doc = get_nlp()(text)
        for sent in doc.sents:
            dependency_tree = self.to_nltk_tree(sent.root)

        if dependency_tree is None:
            raise EmptySyntaxTreeError

        return dependency_tree
