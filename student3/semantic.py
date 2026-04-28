from __future__ import annotations

from dataclasses import dataclass, field

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


class SemanticError(Exception):
    """Raised when semantic validation fails."""


@dataclass
class Scope:
    parent: "Scope | None" = None
    bindings: dict[str, str] = field(default_factory=dict)

    def declare(self, name: str, var_type: str) -> None:
        if name in self.bindings:
            raise SemanticError(f"Duplicate declaration for variable '{name}'.")
        self.bindings[name] = var_type

    def resolve(self, name: str) -> str:
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.resolve(name)
        raise SemanticError(f"Use of undeclared variable '{name}'.")


class SemanticAnalyzer:
    def analyze(self, program: Program) -> None:
        scope = Scope()
        for statement in program.statements:
            self._visit_statement(statement, scope)

    def _visit_statement(self, statement, scope: Scope) -> None:
        if isinstance(statement, Block):
            block_scope = Scope(scope)
            for nested_statement in statement.statements:
                self._visit_statement(nested_statement, block_scope)
            return

        if isinstance(statement, Declaration):
            scope.declare(statement.name, statement.var_type)
            if statement.initializer is not None:
                initializer_type = self._visit_expression(statement.initializer, scope)
                self._ensure_type_match(statement.var_type, initializer_type, statement.name)
            return

        if isinstance(statement, Assignment):
            variable_type = scope.resolve(statement.name)
            expression_type = self._visit_expression(statement.expression, scope)
            self._ensure_type_match(variable_type, expression_type, statement.name)
            return

        if isinstance(statement, IfStatement):
            self._ensure_boolean_condition(statement.condition, scope, "If")
            self._visit_statement(statement.then_branch, scope)
            if statement.else_branch is not None:
                self._visit_statement(statement.else_branch, scope)
            return

        if isinstance(statement, WhileStatement):
            self._ensure_boolean_condition(statement.condition, scope, "While")
            self._visit_statement(statement.body, scope)
            return

        raise SemanticError(f"Unsupported statement type: {type(statement).__name__}")

    def _visit_expression(self, expression, scope: Scope) -> str:
        if isinstance(expression, NumberLiteral):
            return "int"

        if isinstance(expression, Identifier):
            return scope.resolve(expression.name)

        if isinstance(expression, UnaryExpression):
            operand_type = self._visit_expression(expression.operand, scope)
            if expression.operator == "-" and operand_type == "int":
                return "int"
            raise SemanticError(f"Unsupported unary operation '{expression.operator}' for type '{operand_type}'.")

        if isinstance(expression, BinaryExpression):
            left_type = self._visit_expression(expression.left, scope)
            right_type = self._visit_expression(expression.right, scope)

            if expression.operator in {"+", "-", "*", "/"}:
                if left_type == right_type == "int":
                    return "int"
                raise SemanticError(f"Arithmetic operator '{expression.operator}' requires int operands.")

            if expression.operator in {"<", ">"}:
                if left_type == right_type == "int":
                    return "bool"
                raise SemanticError(f"Relational operator '{expression.operator}' requires int operands.")

            if expression.operator == "==":
                if left_type == right_type:
                    return "bool"
                raise SemanticError("Equality comparison requires both operands to have the same type.")

        raise SemanticError(f"Unsupported expression type: {type(expression).__name__}")

    @staticmethod
    def _ensure_type_match(expected: str, actual: str, name: str) -> None:
        if expected != actual:
            raise SemanticError(
                f"Type mismatch for '{name}': expected {expected}, but found {actual}."
            )

    def _ensure_boolean_condition(self, expression, scope: Scope, statement_name: str) -> None:
        if self._visit_expression(expression, scope) != "bool":
            raise SemanticError(f"{statement_name} condition must evaluate to bool.")
