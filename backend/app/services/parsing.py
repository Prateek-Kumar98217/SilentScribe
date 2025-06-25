import ast

def parse_file_to_blocks(file_content: str) -> list[dict]:
    """
    Parse the content of the file and extract code blocks.
    """
    try:
        tree = ast.parse(file_content)
    except SyntaxError:
        raise ValueError("Syntax error in the provided file content")
    
    code_blocks = []

    for node in tree.body:
        block = {
            "type":None,
            "name": getattr(node, "name", None),
            "lineno": getattr(node, "lineno", None),
            "col_offset": getattr(node, "col_offset", None),
            "end_lineno": getattr(node, "end_lineno", None),
            "end_col_offset": getattr(node, "end_col_offset", None),
            "docstring": None,
            "used_names":[],
            "args":[],
            "returns": None,
            "code": ast.get_source_segment(file_content, node) or ast.unparse(node)
        }

        if isinstance(node, ast.FunctionDef):
            block["type"] = "function"
            block["docstring"] = ast.get_docstring(node)
            block["used_names"] = sorted({n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
            block["args"] = [arg.arg for arg in node.args.args]
            block["returns"] = ast.unparse(node.returns) if node.returns else None
        elif isinstance(node, ast.AsyncFunctionDef):
            block["type"] = "asyncfunction"
            block["docstring"] = ast.get_docstring(node)
            block["used_names"] = sorted({n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
            block["args"] = [arg.arg for arg in node.args.args]
            block["returns"] = ast.unparse(node.returns) if node.returns else None
        elif isinstance(node, ast.ClassDef):
            block["type"] = "class"
            block["docstring"] = ast.get_docstring(node)
            block["used_names"] = sorted({n.id for n in ast.walk(node) if isinstance(n, ast.Name)})
        elif isinstance(node, ast.Import):
            block["type"] = "import"
            block["used_names"] = sorted({n.name for n in node.names})
        elif isinstance(node, ast.ImportFrom):
            block["type"] = "import_from"
            block["used_names"] = sorted({n.name for n in node.names})
        else :
            continue

        code_blocks.append(block)
    return code_blocks