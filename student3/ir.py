from __future__ import annotations

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


class IRGenerator:
    def __init__(self) -> None:
        self.temp_counter = 0
        self.label_counter = 0
        self.instructions: list[str] = []

    def generate(self, program: Program) -> list[str]:
        self.temp_counter = 0
        self.label_counter = 0
        self.instructions = []
        self._emit_statements(program.statements)
        return self.instructions

    def _emit_statements(self, statements) -> None:
        for statement in statements:
            self._emit_statement(statement)

    def _emit_statement(self, statement) -> None:
        if isinstance(statement, Block):
            self._emit_statements(statement.statements)
            return

        if isinstance(statement, Declaration):
            if statement.initializer is not None:
                value = self._emit_expression(statement.initializer)
                self.instructions.append(f"{statement.name} = {value}")
            return

        if isinstance(statement, Assignment):
            value = self._emit_expression(statement.expression)
            self.instructions.append(f"{statement.name} = {value}")
            return

        if isinstance(statement, IfStatement):
            true_label = self._new_label()
            end_label = self._new_label()
            false_label = self._new_label() if statement.else_branch is not None else end_label
            condition = self._emit_expression(statement.condition)
            self.instructions.append(f"if {condition} goto {true_label}")
            self.instructions.append(f"goto {false_label}")
            self.instructions.append(f"{true_label}:")
            self._emit_statement(statement.then_branch)
            if statement.else_branch is not None:
                self.instructions.append(f"goto {end_label}")
                self.instructions.append(f"{false_label}:")
                self._emit_statement(statement.else_branch)
            self.instructions.append(f"{end_label}:")
            return

        if isinstance(statement, WhileStatement):
            start_label = self._new_label()
            body_label = self._new_label()
            end_label = self._new_label()
            self.instructions.append(f"{start_label}:")
            condition = self._emit_expression(statement.condition)
            self.instructions.append(f"if {condition} goto {body_label}")
            self.instructions.append(f"goto {end_label}")
            self.instructions.append(f"{body_label}:")
            self._emit_statement(statement.body)
            self.instructions.append(f"goto {start_label}")
            self.instructions.append(f"{end_label}:")
            return

        raise ValueError(f"Unsupported statement type: {type(statement).__name__}")

    def _emit_expression(self, expression) -> str:
        if isinstance(expression, NumberLiteral):
            return str(expression.value)

        if isinstance(expression, Identifier):
            return expression.name

        if isinstance(expression, UnaryExpression):
            operand = self._emit_expression(expression.operand)
            temp = self._new_temp()
            self.instructions.append(f"{temp} = {expression.operator}{operand}")
            return temp

        if isinstance(expression, BinaryExpression):
            left = self._emit_expression(expression.left)
            right = self._emit_expression(expression.right)
            temp = self._new_temp()
            self.instructions.append(f"{temp} = {left} {expression.operator} {right}")
            return temp

        raise ValueError(f"Unsupported expression type: {type(expression).__name__}")

    def _new_temp(self) -> str:
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def _new_label(self) -> str:
        self.label_counter += 1
        return f"L{self.label_counter}"
