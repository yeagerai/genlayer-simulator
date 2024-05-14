from genvm.utils import code_enforcement_check


def test_bad_code():
    with open("genvm/tests/code/broken_code.py", "r") as f:
        broken_code = f.read()
        result = code_enforcement_check(broken_code, "A")
        result["status"] == "error"
        result["message"] == "Your code is not valid Python code"
        result["data"] = []

def test_good_code():
    with open("genvm/tests/code/working_code.py", "r") as f:
        working_code = f.read()
        result = code_enforcement_check(working_code, "A")
        result["status"] = "success"
        result["message"] = ""
        result["data"] = []

def test_good_code_class_does_not_exist():
    with open("genvm/tests/code/working_code.py", "r") as f:
        class_name = "ThisClassDoesNotExist"
        working_code = f.read()
        result = code_enforcement_check(working_code, class_name)
        result["status"] = "error"
        result["message"] = f"The class {class_name} does not exist in the code"
        result["data"] = []

def test_catch_direct_instatntiation_of_eq_principle():
    with open("genvm/tests/code/bad_eq_implementation.py", "r") as f:
        bad_eq_implementation = f.read()
        result = code_enforcement_check(bad_eq_implementation, "A")
        result["status"] == "error"
        result["message"] == "You cannot directly instantiate the EquivalencePrinciple class"
        result["data"] = []

def test_inside_eq_with_block_modifys_self():
    with open("genvm/tests/code/bad_eq_modifys_self.py", "r") as f:
        bad_eq_modifys_self = f.read()
        result = code_enforcement_check(bad_eq_modifys_self, "A")
        result["status"] == "error"
        result["message"] == "Self was modified inside an equivalence block"
        result["data"] = [15]

def test_eq_block_variables_not_accessed_outsode_of_block():
    with open("genvm/tests/code/bad_eq_variables_accessed_outside_of_block.py", "r") as f:
        bad_eq_variables_accessed_outside_of_block = f.read()
        result = code_enforcement_check(bad_eq_variables_accessed_outside_of_block, "A")
        result["status"] == "error"
        result["message"] == "Variables declared in the equivalence block are referenced outside of the equivalence block"
        result["data"] = [17]

def test_eq_block_variables_not_accessed_outsode_of_block_complex():
    with open("genvm/tests/code/bad_eq_variables_accessed_outside_of_block_complex.py", "r") as f:
        bad_eq_variables_accessed_outside_of_block = f.read()
        result = code_enforcement_check(bad_eq_variables_accessed_outside_of_block, "B")
        result["status"] == "error"
        result["message"] == "Variables declared in the equivalence block are referenced outside of the equivalence block"
        result["data"] = [18,28,29]

