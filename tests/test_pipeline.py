from __future__ import annotations

import unittest
from pathlib import Path

from main import run_pipeline
from student1.lexer import LexerError
from student2.parser import ParserError
from student3.semantic import SemanticError

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


class PipelineTests(unittest.TestCase):
    def test_valid_program_runs_full_pipeline(self) -> None:
        source = self._read_example("valid_program.tl")
        result = run_pipeline(source)
        self.assertTrue(result["ir"])
        self.assertEqual(result["tokens"][-1].lexeme, "")

    def test_semantic_errors_are_rejected(self) -> None:
        cases = [
            ("invalid_undeclared.tl", SemanticError),
            ("invalid_duplicate.tl", SemanticError),
            ("invalid_type_mismatch.tl", SemanticError),
        ]
        for filename, error_type in cases:
            with self.subTest(filename=filename):
                with self.assertRaises(error_type):
                    run_pipeline(self._read_example(filename))

    def test_lexer_and_parser_errors_are_rejected(self) -> None:
        invalid_sources = [
            ("int x; x = 1 @ 2;", LexerError),
            ("int x\nx = 1;", ParserError),
        ]
        for source, error_type in invalid_sources:
            with self.subTest(error=error_type.__name__):
                with self.assertRaises(error_type):
                    run_pipeline(source)

    @staticmethod
    def _read_example(filename: str) -> str:
        return (EXAMPLES_DIR / filename).read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
