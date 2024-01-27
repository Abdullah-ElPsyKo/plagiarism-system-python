import ast

def get_ast_string(code):
    try:
        tree = ast.parse(code)
        return ast.dump(tree)
    except SyntaxError:
        return None


def are_asts_identical(code1, code2):
    ast1 = get_ast_string(code1)
    ast2 = get_ast_string(code2)
    return ast1 is not None and ast2 is not None and ast1 == ast2
