from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any


class AstNode:
    def to_dict(self) -> dict[str, Any]:
        return _serialize(self)


def _serialize(value: Any) -> Any:
    if is_dataclass(value):
        data = {"node": type(value).__name__}
        for field_info in fields(value):
            data[field_info.name] = _serialize(getattr(value, field_info.name))
        return data
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    return value


class Statement(AstNode):
    pass


class Expression(AstNode):
    pass


@dataclass
class Program(AstNode):
    statements: list[Statement] = field(default_factory=list)


@dataclass
class Block(Statement):
    statements: list[Statement] = field(default_factory=list)


@dataclass
class Declaration(Statement):
    name: str
    initializer: Expression | None = None
    var_type: str = "int"


@dataclass
class Assignment(Statement):
    name: str
    expression: Expression


@dataclass
class IfStatement(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Statement | None = None


@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: Statement


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass
class UnaryExpression(Expression):
    operator: str
    operand: Expression


@dataclass
class NumberLiteral(Expression):
    value: int


@dataclass
class Identifier(Expression):
    name: str
