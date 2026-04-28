from __future__ import annotations

from student1.tokens import Token, TokenType
from student2.ast_nodes import (
    Assignment,
    BinaryExpression,
    Block,
    Declaration,
    Identifier,
    IfStatement,
    NumberLiteral,
    Program,
    UnaryExpression,
    WhileStatement,
)


class ParserError(Exception):
    """Raised when the token stream violates the TinyLang grammar."""


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements = []
        while not self._check(TokenType.EOF):
            statements.append(self._statement())
        self._consume(TokenType.EOF, "Expected end of file.")
        return Program(statements)

    def _statement(self):
        if self._match(TokenType.INT):
            return self._declaration()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.LBRACE):
            return self._block()
        return self._assignment_statement()

    def _declaration(self) -> Declaration:
        name = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'int'.")
        initializer = None
        if self._match(TokenType.ASSIGN):
            initializer = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after declaration.")
        return Declaration(name.lexeme, initializer)

    def _assignment_statement(self) -> Assignment:
        name = self._consume(TokenType.IDENTIFIER, "Expected identifier at start of assignment.")
        self._consume(TokenType.ASSIGN, "Expected '=' in assignment.")
        expression = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after assignment.")
        return Assignment(name.lexeme, expression)

    def _if_statement(self) -> IfStatement:
        self._consume(TokenType.LPAREN, "Expected '(' after 'if'.")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after if condition.")
        then_branch = self._statement()
        else_branch = self._statement() if self._match(TokenType.ELSE) else None
        return IfStatement(condition, then_branch, else_branch)

    def _while_statement(self) -> WhileStatement:
        self._consume(TokenType.LPAREN, "Expected '(' after 'while'.")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after while condition.")
        body = self._statement()
        return WhileStatement(condition, body)

    def _block(self) -> Block:
        statements = []
        while not self._check(TokenType.RBRACE) and not self._check(TokenType.EOF):
            statements.append(self._statement())
        self._consume(TokenType.RBRACE, "Expected '}' to close block.")
        return Block(statements)

    def _expression(self):
        return self._equality()

    def _equality(self):
        return self._parse_left_associative(self._comparison, TokenType.EQUAL_EQUAL)

    def _comparison(self):
        return self._parse_left_associative(self._term, TokenType.LESS, TokenType.GREATER)

    def _term(self):
        return self._parse_left_associative(self._factor, TokenType.PLUS, TokenType.MINUS)

    def _factor(self):
        return self._parse_left_associative(self._unary, TokenType.STAR, TokenType.SLASH)

    def _unary(self):
        if self._match(TokenType.MINUS):
            return UnaryExpression("-", self._unary())
        return self._primary()

    def _primary(self):
        if self._match(TokenType.NUMBER):
            return NumberLiteral(int(self._previous().lexeme))
        if self._match(TokenType.IDENTIFIER):
            return Identifier(self._previous().lexeme)
        if self._match(TokenType.LPAREN):
            expression = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expression

        token = self._peek()
        raise ParserError(
            f"Unexpected token {token.token_type.name} ({token.lexeme!r}) "
            f"at line {token.line}, column {token.column}."
        )

    def _parse_left_associative(self, operand_parser, *operators: TokenType):
        expression = operand_parser()
        while self._match(*operators):
            expression = BinaryExpression(expression, self._previous().lexeme, operand_parser())
        return expression

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        token = self._peek()
        raise ParserError(f"{message} Found {token.token_type.name} at line {token.line}, column {token.column}.")

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return token_type == TokenType.EOF
        return self._peek().token_type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _is_at_end(self) -> bool:
        return self.tokens[self.current].token_type == TokenType.EOF
