from __future__ import annotations

from student1.tokens import KEYWORDS, Token, TokenType

SINGLE_CHAR_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
    ";": TokenType.SEMICOLON,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
}


class LexerError(Exception):
    """Raised when the lexer encounters invalid input."""


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        while not self._is_at_end():
            char = self._peek()

            if char in {" ", "\r", "\t"}:
                self._advance()
                continue

            if char == "\n":
                self._advance()
                self.line += 1
                self.column = 1
                continue

            if char == "/" and self._peek_next() == "/":
                self._skip_comment()
                continue

            start_line = self.line
            start_column = self.column

            if char.isalpha() or char == "_":
                lexeme = self._consume_identifier()
                token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
                tokens.append(Token(token_type, lexeme, start_line, start_column))
                continue

            if char.isdigit():
                lexeme = self._consume_number()
                tokens.append(Token(TokenType.NUMBER, lexeme, start_line, start_column))
                continue

            token = self._consume_symbol(start_line, start_column)
            if token is None:
                raise LexerError(
                    f"Unexpected character {char!r} at line {start_line}, column {start_column}"
                )
            tokens.append(token)

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    def _consume_symbol(self, line: int, column: int) -> Token | None:
        char = self._advance()

        if char == "=":
            if self._match("="):
                return Token(TokenType.EQUAL_EQUAL, "==", line, column)
            return Token(TokenType.ASSIGN, "=", line, column)

        token_type = SINGLE_CHAR_TOKENS.get(char)
        if token_type is None:
            return None
        return Token(token_type, char, line, column)

    def _consume_identifier(self) -> str:
        start = self.index
        while not self._is_at_end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()
        return self.source[start:self.index]

    def _consume_number(self) -> str:
        start = self.index
        while not self._is_at_end() and self._peek().isdigit():
            self._advance()
        return self.source[start:self.index]

    def _skip_comment(self) -> None:
        while not self._is_at_end() and self._peek() != "\n":
            self._advance()

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.index] != expected:
            return False
        self._advance()
        return True

    def _peek(self) -> str:
        return self.source[self.index]

    def _peek_next(self) -> str:
        if self.index + 1 >= len(self.source):
            return "\0"
        return self.source[self.index + 1]

    def _advance(self) -> str:
        char = self.source[self.index]
        self.index += 1
        self.column += 1
        return char

    def _is_at_end(self) -> bool:
        return self.index >= len(self.source)
