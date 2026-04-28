# Mini Compiler Front-End for TinyLang

This project is a Python compiler front-end for a small language called `TinyLang`. It includes the required stages:

- lexical analysis
- parsing
- AST construction
- semantic analysis
- three-address-code generation

## Project Layout

```text
mini-compiler-frontend/
├── main.py
├── README.md
├── examples/
├── student1/
├── student2/
├── student3/
└── tests/
```

## Student Split

### Student 1: Lexer + Tokens

- [student1/tokens.py](/Users/caseydane/Documents/CS/Projects/mini-compiler-frontend/student1/tokens.py)
- [student1/lexer.py](/Users/caseydane/Documents/CS/Projects/mini-compiler-frontend/student1/lexer.py)
- handles keywords, identifiers, numbers, operators, delimiters, and lexical errors

### Student 2: Parser + AST

- [student2/parser.py](/Users/caseydane/Documents/CS/Projects/mini-compiler-frontend/student2/parser.py)
- [student2/ast_nodes.py](/Users/caseydane/Documents/CS/Projects/mini-compiler-frontend/student2/ast_nodes.py)
- handles recursive-descent parsing, precedence, AST building, and syntax errors

### Student 3: Semantic Analysis + IR

- [student3/semantic.py](/Users/caseydane/Documents/CS/Projects/mini-compiler-frontend/student3/semantic.py)
- [student3/ir.py](/Users/caseydane/Documents/CS/Projects/mini-compiler-frontend/student3/ir.py)
- handles symbol tables, nested scope, semantic checks, and three-address code

## Shared Work

- language design
- testing valid and invalid programs
- debugging
- presentation/demo prep

## Supported Features

- variable declarations: `int x;`
- assignment statements
- arithmetic: `+`, `-`, `*`, `/`
- relational operators: `<`, `>`, `==`
- `if-else`
- `while`
- block scope with `{ ... }`

## Grammar

```ebnf
program        -> statement* EOF ;
statement      -> declaration | assignment | ifStatement | whileStatement | block ;
declaration    -> "int" IDENTIFIER ( "=" expression )? ";" ;
assignment     -> IDENTIFIER "=" expression ";" ;
ifStatement    -> "if" "(" expression ")" statement ( "else" statement )? ;
whileStatement -> "while" "(" expression ")" statement ;
block          -> "{" statement* "}" ;
expression     -> equality ;
equality       -> comparison ( "==" comparison )* ;
comparison     -> term ( ( "<" | ">" ) term )* ;
term           -> factor ( ( "+" | "-" ) factor )* ;
factor         -> unary ( ( "*" | "/" ) unary )* ;
unary          -> "-" unary | primary ;
primary        -> NUMBER | IDENTIFIER | "(" expression ")" ;
```

## Semantic Checks

- undeclared variables
- duplicate declarations in the same scope
- basic type mismatch
- non-boolean `if` conditions
- non-boolean `while` conditions

## How to Run

```bash
python3 main.py
python3 main.py examples/valid_program.tl
python3 -m unittest discover -s tests -v
```

## Sample Files

- valid input: `examples/valid_program.tl`
- undeclared variable: `examples/invalid_undeclared.tl`
- duplicate declaration: `examples/invalid_duplicate.tl`
- type mismatch: `examples/invalid_type_mismatch.tl`
