import libcst as cst
from spellchecker import SpellChecker

class LexiconCollector(cst.CSTVisitor):
    def __init__(self):
        self.words = set()

    def visit_SimpleString(self, node):
        stripped_string = node.value.strip("\"'")  # remove single quotes
        self.words.update(stripped_string.split())

    def visit_Name(self, node):
        # Verzamel namen van variabelen
        self.words.add(node.value)

def check_spelling_errors(code):
    collector = LexiconCollector()
    cst_tree = cst.parse_module(code)
    cst_tree.visit(collector)
    spell = SpellChecker()
    unknown_words = spell.unknown(collector.words)
    return unknown_words

if __name__ == "__main__":
    code = 'variable = "hello i\'m a string literal and i hve a typo in me"'
    print(check_spelling_errors(code))
