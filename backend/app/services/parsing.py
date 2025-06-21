import ast

NODE_TYPE_MAP = {
    ast.FunctionDef: "function",
    ast.AsyncFunctionDef: "async function",
    ast.ClassDef: "class",
    ast.Import: "import",
    ast.ImportFrom: "import_from"
}

def extract_ast_metadata(code: str) -> dict:
    try:
        tree = ast.parse(code)
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

def get_node_content(node: ast)-> str:
    """
    Extract the source code from AST nodes
    """