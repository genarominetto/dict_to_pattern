import ast
import difflib
import os

class IntelligentDiff:
    def __init__(self):
        pass

    def _parse_ast(self, file_path):
        """Parse a Python file into an AST."""
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
        return ast.parse(file_content, filename=os.path.basename(file_path))

    def _normalize_ast(self, node):
        """Normalize AST by removing docstrings and other non-logical elements."""
        if isinstance(node, ast.Module):
            node.body = [self._normalize_ast(n) for n in node.body if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Str)]
        elif isinstance(node, ast.FunctionDef):
            node.body = [self._normalize_ast(n) for n in node.body if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Str)]
        elif isinstance(node, ast.ClassDef):
            node.body = [self._normalize_ast(n) for n in node.body if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Str)]
        elif isinstance(node, list):
            return [self._normalize_ast(n) for n in node]
        elif hasattr(node, "_fields"):
            for field in node._fields:
                setattr(node, field, self._normalize_ast(getattr(node, field)))
        return node

    def _ast_to_code(self, node):
        """Convert AST node back to code."""
        return ast.unparse(node)

    def _get_diff(self, content1, content2):
        """Get the diff between two sets of content."""
        diff = difflib.unified_diff(content1, content2)
        return "\n".join(diff)

    def _is_equivalent(self, ast1, ast2):
        """Check if two ASTs are logically equivalent."""
        return ast.dump(ast1) == ast.dump(ast2)

    def _compare_files(self, file1, file2):
        """Compare two files, using AST for Python files and regular diff for others."""
        if file1.endswith('.py') and file2.endswith('.py'):
            ast1 = self._normalize_ast(self._parse_ast(file1))
            ast2 = self._normalize_ast(self._parse_ast(file2))
            if self._is_equivalent(ast1, ast2):
                return None  # No differences
            else:
                code1 = self._ast_to_code(ast1).splitlines()
                code2 = self._ast_to_code(ast2).splitlines()
                return self._get_diff(code1, code2)
        else:
            with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
                content1 = f1.read().splitlines()
                content2 = f2.read().splitlines()
                return self._get_diff(content1, content2)

    def compare_directories(self, dir1_path, dir2_path):
        """Compare two directories and return differences."""
        differences = []
        for dirpath, _, filenames in os.walk(dir1_path):
            for filename in filenames:
                file1 = os.path.join(dirpath, filename)
                file2 = os.path.join(dir2_path, os.path.relpath(file1, dir1_path))
                if os.path.exists(file2):
                    diff = self._compare_files(file1, file2)
                    if diff:
                        differences.append((file1, file2, diff))
                else:
                    differences.append((file1, file2, "File does not exist in second directory."))
        for dirpath, _, filenames in os.walk(dir2_path):
            for filename in filenames:
                file2 = os.path.join(dirpath, filename)
                file1 = os.path.join(dir1_path, os.path.relpath(file2, dir2_path))
                if not os.path.exists(file1):
                    differences.append((file1, file2, "File does not exist in first directory."))
        return differences

