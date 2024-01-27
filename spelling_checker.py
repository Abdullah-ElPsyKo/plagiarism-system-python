import libcst as cst
from spellchecker import SpellChecker

class LexiconCollector(cst.CSTVisitor):
    def __init__(self):
        self.words = set()


    def visit_SimpleString(self, node):
        stripped_string = node.value.strip("\"'")
        self.words.update(stripped_string.split())


    def visit_Name(self, node):
        self.words.add(node.value)


    def visit_Comment(self, node):
        comment_text = node.value.strip("# ")
        self.words.update(comment_text.split())


def check_spelling_errors(code):
    collector = LexiconCollector()
    cst_tree = cst.parse_module(code)
    cst_tree.visit(collector)
    spell = SpellChecker()
    unknown_words = spell.unknown(collector.words)
    return unknown_words


