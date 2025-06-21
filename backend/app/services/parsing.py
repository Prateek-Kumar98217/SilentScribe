import ast

NODE_TYPE_MAP = {
    ast.FunctionDef: "function",
    ast.AsyncFunctionDef: "async function",
    ast.ClassDef: "class",
    ast.Import: "import",
    ast.ImportFrom: "import_from"
}

def extract_ast_metadata(source_code: str) -> dict:
    """
    Extract metadata from Python code using AST parsing.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        print(f"Syntax error in code: {e}")
        return {"error": str(e)}
    structure = []
    for node in ast.walk(tree):
        node_type = type(node)
        if node_type not in NODE_TYPE_MAP:
            continue
        base_info = {
            "type": NODE_TYPE_MAP[node_type],
            "lineno": getattr(node, "lineno", None),
            "col_offset": getattr(node, "col_offset", None)
        }
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            base_info["name"] = node.name

        elif isinstance(node, ast.Import):
            base_info["names"] = [alias.name for alias in node.names]

        elif isinstance(node, ast.ImportFrom):
            base_info["module"] = node.module
            base_info["names"] = [alias.name for alias in node.names]
        structure.append(base_info)
    return structure

def get_node_content(node: ast.AST, source_code: str)-> str:
    """
    Extract the source code from AST nodes
    """
    node_type = type(node)
    if node_type not in NODE_TYPE_MAP:
        return None
    
    content = {
        "type": NODE_TYPE_MAP[node_type],
        "lineno": getattr(node, "lineno", None),
        "col_offset": getattr(node, "col_offset", None),
        "end_lineno": getattr(node, "end_lineno", None),
        "end_col_offset": getattr(node, "end_col_offset", None),
        "code": ast.get_source_segment(source_code, node) or ast.unparse(node)
    }
    
    if hasattr(node, "name"):
        content["name"] = node.name

    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        content["args"] = [arg.arg for arg in node.args.args]
        content["returns"] = ast.unparse(node.returns) if node.returns else None

    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        content["docstring"] = ast.get_docstring(node)
        content["used_names"] = sorted({
            n.id for n in ast.walk(node) if isinstance(n, ast.Name)
        })

    if isinstance(node, ast.Import):
        content["names"] = [alias.name for alias in node.names]

    if isinstance(node, ast.ImportFrom):
        content["module"] = node.module
        content["names"] = [alias.name for alias in node.names]

    return content