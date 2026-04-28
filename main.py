from __future__ import annotations

import json
import sys
from pathlib import Path

from student1.lexer import Lexer, LexerError
from student2.parser import Parser, ParserError
from student3.ir import IRGenerator
from student3.semantic import SemanticAnalyzer, SemanticError


DEFAULT_PROGRAM = """\
int x;
int y;
x = 3;
y = x + 2 * 5;
if (x < y) {
    int z;
    z = y - x;
} else {
    y = y + 1;
}
while (x < 10) {
    x = x + 1;
}
"""


def run_pipeline(source: str) -> dict[str, object]:
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    SemanticAnalyzer().analyze(ast)
    ir = IRGenerator().generate(ast)
    return {"tokens": tokens, "ast": ast, "ir": ir}


def main() -> int:
    source = _read_source(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_PROGRAM

    try:
        result = run_pipeline(source)
    except (LexerError, ParserError, SemanticError) as error:
        print(f"Compilation failed: {error}")
        return 1

    print("=== TOKENS ===")
    for token in result["tokens"]:
        print(token)

    print("\n=== AST ===")
    print(json.dumps(result["ast"].to_dict(), indent=2))

    print("\n=== THREE-ADDRESS CODE ===")
    for instruction in result["ir"]:
        print(instruction)

    print("\nCompilation succeeded.")
    return 0


def _read_source(args: list[str]) -> str:
    path = Path(args[0])
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
