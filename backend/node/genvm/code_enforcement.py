import ast


def code_enforcement_check(code: str, class_name: str) -> str:
    result = {"status": "error", "message": "", "data": []}
    # Check is valid Python code
    code_check_result = _check_code(code)
    if code_check_result:
        result["message"] = code_check_result
        return result
    # See if the class exists
    if not _does_class_exist_in_code(code, class_name):
        result["message"] = f"The class {class_name} does not exist in the code"
        return result
    # Make sure there are no raw instantiations of the EquivalencePrinciple class
    if _code_has_bad_implementations_of_eq_principle(code):
        result["message"] = (
            "You cannot directly instantiate the EquivalencePrinciple class"
        )
        return result
    # Make sure that no code modifies self inside an equivalence block
    linenos_list = _linenos_of_where_code_modifys_self_in_eq_block(code, class_name)
    if len(linenos_list):
        result["message"] = "Self was modified inside an equivalence block"
        result["data"] = linenos_list
        return result
    # Make sure no equivalence block variables are referenced outside the block
    linenos_list = _code_references_eq_block_variables(code, class_name)
    if len(linenos_list):
        result["message"] = (
            "Variables declared in the equivalence block are referenced outside of the equivalence block"
        )
        result["data"] = linenos_list
        return result
    result["status"] = "success"
    return result


def _check_code(code: str):
    try:
        ast.parse(code)
        return None
    except Exception:
        return "Your code is not valid Python code"


def _does_class_exist_in_code(code: str, class_name: str) -> bool:
    visitor = ClassExistsVisitor(class_name)
    visitor.visit(ast.parse(code))
    return visitor.class_exists


# Visits each class in the code and checks if the
# class name matches the class name poassed in
class ClassExistsVisitor(ast.NodeVisitor):
    def __init__(self, class_name):
        self.class_name = class_name
        self.class_exists = False

    def visit_ClassDef(self, node):
        if node.name == self.class_name:
            self.class_exists = True
        self.generic_visit(node)


def _code_has_bad_implementations_of_eq_principle(code: str) -> bool:
    visitor = EquivalencePrincipleVisitor()
    visitor.visit(ast.parse(code))
    if visitor.all_eq_line_nums != visitor.eq_line_nums_inside_async_waith_blocks:
        return True
    return False


class EquivalencePrincipleVisitor(ast.NodeVisitor):

    def __init__(self):
        self.all_eq_line_nums = []
        self.eq_line_nums_inside_async_waith_blocks = []

    # All the places where the EquivalencePrinciple class is called
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "EquivalencePrinciple":
            self.eq_line_nums_inside_async_waith_blocks.append(node.lineno)
        self.generic_visit(node)

    # All the places where the EquivalencePrinciple class is called within an async with block
    def visit_AsyncWith(self, node):
        async_ctx = node.items[0].context_expr
        if isinstance(async_ctx, ast.Call) and isinstance(async_ctx.func, ast.Name):
            if async_ctx.func.id == "EquivalencePrinciple":
                self.all_eq_line_nums.append(node.lineno)
        self.generic_visit(node)


def _linenos_of_where_code_modifys_self_in_eq_block(code: str, class_name) -> bool:
    visitor = EquivalencePrincipleModifySelfVisitor(class_name)
    visitor.visit(ast.parse(code))
    return visitor.modeifies_self_linenos


class EquivalencePrincipleModifySelfVisitor(ast.NodeVisitor):

    def __init__(self, class_name):
        self.class_name = class_name
        self.inside_call_method = False
        self.inside_eq_block = False
        self.modeifies_self_linenos = []

    # Mark the fact that we are inside the code's class method
    def visit_ClassDef(self, node):
        if node.name == self.class_name:
            for body_item in node.body:
                if (
                    isinstance(body_item, ast.AsyncFunctionDef)
                    and body_item.name != "__init__"
                ):
                    self.inside_call_method = True
                    self.generic_visit(body_item)
                    self.inside_call_method = False

    # Mark thew fact that we are inside an equivalence block
    def visit_AsyncWith(self, node):
        async_ctx = node.items[0].context_expr
        if isinstance(async_ctx, ast.Call) and isinstance(async_ctx.func, ast.Name):
            if async_ctx.func.id == "EquivalencePrinciple":
                self.inside_eq_block = True
                self.generic_visit(node)
                self.inside_eq_block = False

    # Record all assignments of class variables done inside an
    # equivalence block
    def visit_Assign(self, node):
        for target in node.targets:
            if self.inside_call_method and self.inside_eq_block:
                if (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                ):
                    self.modeifies_self_linenos.append(target.lineno)
        self.generic_visit(node)


def _code_references_eq_block_variables(code: str, class_name: str) -> list:
    visitor = EquivalencePrincipleBlockVariables(class_name)
    visitor.visit(ast.parse(code))
    return visitor.referenced_block_variables


class EquivalencePrincipleBlockVariables(ast.NodeVisitor):

    def __init__(self, class_name: str):
        self.class_name = class_name
        self.inside_call_method = False
        self.inside_eq_block = False
        self.has_visited_eq_block = False
        self.eq_block_variables = []
        self.referenced_block_variables = []

    # Mark the fact that we are inside the code's class method
    def visit_ClassDef(self, node):
        if node.name == self.class_name:
            for body_item in node.body:
                if (
                    isinstance(body_item, ast.AsyncFunctionDef)
                    and body_item.name != "__init__"
                ):
                    self.inside_call_method = True
                    self.generic_visit(body_item)
                    self.inside_call_method = False

    # Mark the fact that we are inside an equivalence block
    # (and have visited at least one equivalence block)
    def visit_AsyncWith(self, node):
        async_ctx = node.items[0].context_expr
        if isinstance(async_ctx, ast.Call) and isinstance(async_ctx.func, ast.Name):
            if async_ctx.func.id == "EquivalencePrinciple":
                self.inside_eq_block = True
                self.generic_visit(node)
                self.inside_eq_block = False
                self.has_visited_eq_block = True

    # Records all the variables declared inside an equivalence block
    def visit_Assign(self, node):
        for target in node.targets:
            if (
                isinstance(target, ast.Name)
                and self.inside_call_method
                and self.inside_eq_block
            ):
                self.eq_block_variables.append(target.id)
        self.generic_visit(node)

    # Records all the variables declared in an equivalence block
    # that are referenced outside of it
    def visit_Name(self, node):
        if (
            self.inside_call_method
            and not self.inside_eq_block
            and node.id in self.eq_block_variables
        ):
            self.referenced_block_variables.append(node.lineno)
