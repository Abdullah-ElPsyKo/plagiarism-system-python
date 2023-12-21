import libcst as cst

class RemoveCommentsTransformer(cst.CSTTransformer):
    def leave_Comment(self, original_node, updated_node):
        return cst.RemoveFromParent()
    
    
def check_cst_comments(line1, line2):
    cst1 = cst.parse_module(line1)
    cst2 = cst.parse_module(line2)
    
    tree1 = cst1.visit(RemoveCommentsTransformer())
    tree2 = cst2.visit(RemoveCommentsTransformer())

    return tree1.deep_equals(tree2)


