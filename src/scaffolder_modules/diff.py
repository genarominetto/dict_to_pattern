import ast
import difflib
import os

class IntelligentDiff:
    def __init__(self, file1_path=None, file2_path=None):
        self.file1_path = file1_path
        self.file2_path = file2_path
        if file1_path and file2_path:
            self.file1_ast = self.parse_ast(file1_path)
            self.file2_ast = self.parse_ast(file2_path)
            self.normalized_ast1 = self.normalize_ast(self.file1_ast)
            self.normalized_ast2 = self.normalize_ast(self.file2_ast)

    def parse_ast(self, file_path):
        """Parse a Python file into an AST."""
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
        return ast.parse(file_content, filename=os.path.basename(file_path))

    def normalize_ast(self, node):
        """Normalize AST by removing docstrings and other non-logical elements."""
        if isinstance(node, ast.Module):
            node.body = [self.normalize_ast(n) for n in node.body if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Str)]
        elif isinstance(node, ast.FunctionDef):
            node.body = [self.normalize_ast(n) for n in node.body if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Str)]
        elif isinstance(node, ast.ClassDef):
            node.body = [self.normalize_ast(n) for n in node.body if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Str)]
        elif isinstance(node, list):
            return [self.normalize_ast(n) for n in node]
        elif hasattr(node, "_fields"):
            for field in node._fields:
                setattr(node, field, self.normalize_ast(getattr(node, field)))
        return node

    def ast_to_code(self, node):
        """Convert AST node back to code."""
        return ast.unparse(node)

    def get_diff(self):
        """Get the intelligent diff between two Python files."""
        code1 = self.ast_to_code(self.normalized_ast1).splitlines()
        code2 = self.ast_to_code(self.normalized_ast2).splitlines()
        diff = difflib.unified_diff(code1, code2, fromfile=self.file1_path, tofile=self.file2_path)
        return "\n".join(diff)

    def is_equivalent(self):
        """Check if the two Python files are logically equivalent."""
        return ast.dump(self.normalized_ast1) == ast.dump(self.normalized_ast2)

