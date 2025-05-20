import re

KEYWORDS = {"fn", "let", "return"}
SYMBOLS = {"(", ")", "{", "}", ";", "=", "+", "-", "*", "&"}

def tokenize(code):
    tokens = []
    i = 0
    while i < len(code):
        c = code[i]
        if c.isspace():
            i += 1
            continue
        elif c.isalpha() or c == '_':
            start = i
            while i < len(code) and (code[i].isalnum() or code[i] == '_'):
                i += 1
            word = code[start:i]
            if word in KEYWORDS:
                tokens.append(("KEYWORD", word))
            else:
                tokens.append(("IDENT", word))
        elif c.isdigit():
            start = i
            while i < len(code) and code[i].isdigit():
                i += 1
            tokens.append(("INT", int(code[start:i])))
        elif c in SYMBOLS:
            tokens.append(("SYMBOL", c))
            i += 1
        else:
            raise ValueError(f"Unexpected character: {c}")
    return tokens

class ASTNode:
    pass

class Function(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class Let(ASTNode):
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class IntLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class Var(ASTNode):
    def __init__(self, name):
        self.name = name


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        token = self.peek()
        self.pos += 1
        return token

    def expect(self, kind, value=None):
        tok = self.consume()
        if tok[0] != kind or (value is not None and tok[1] != value):
            raise SyntaxError(f"Expected {kind} {value}, got {tok}")
        return tok

    def parse_expr(self):
        left = self.parse_term()
        while self.peek() and self.peek()[0] == "SYMBOL" and self.peek()[1] in {"+", "-"}:
            op = self.consume()[1]
            right = self.parse_term()
            left = BinOp(left, op, right)
        return left

    def parse_term(self):
        tok = self.peek()
        if tok[0] == "INT":
            return IntLiteral(self.consume()[1])
        elif tok[0] == "IDENT":
            return Var(self.consume()[1])
        else:
            raise SyntaxError(f"Unexpected token: {tok}")

    def parse_let(self):
        self.expect("KEYWORD", "let")
        varname = self.expect("IDENT")[1]
        self.expect("SYMBOL", "=")
        expr = self.parse_expr()
        self.expect("SYMBOL", ";")
        return Let(varname, expr)

    def parse_function(self):
        self.expect("KEYWORD", "fn")
        name = self.expect("IDENT")[1]
        self.expect("SYMBOL", "(")
        self.expect("SYMBOL", ")")
        self.expect("SYMBOL", "{")
        body = []
        while self.peek() and self.peek()[1] != "}":
            body.append(self.parse_let())
        self.expect("SYMBOL", "}")
        return Function(name, body)


class CodeGen:
    def __init__(self,offset):
        self.asm = []
        self.memory_map = {}  # e.g., x -> address
        self.next_free = offset  # skip some memory for MMIO

    def alloc(self, varname):
        if varname not in self.memory_map:
            self.memory_map[varname] = self.next_free
            self.next_free += 1
        return self.memory_map[varname]
    
    def emit_expr(self, expr):
        if isinstance(expr, IntLiteral):
            addr = self.next_free
            self.next_free += 1
            self.asm.append(f"CPi {addr}, {expr.value}")
            return addr
        elif isinstance(expr, Var):
            return self.memory_map[expr.name]
        elif isinstance(expr, BinOp):
            left_addr = self.emit_expr(expr.left)
            right_addr = self.emit_expr(expr.right)
            result_addr = self.next_free
            self.next_free += 1
            if expr.op == "+":
                self.asm.append(f"ADD {result_addr}, {left_addr}, {right_addr}")
            else:
                raise NotImplementedError()
            return result_addr

    def emit_let(self, letstmt):
        val_addr = self.emit_expr(letstmt.expr)
        target = self.alloc(letstmt.varname)
        self.asm.append(f"CP {target}, {val_addr}")

    def emit_function(self, fn):
        for stmt in fn.body:
            if isinstance(stmt, Let):
                self.emit_let(stmt)

    def generate(self, ast):
        self.emit_function(ast)
        return self.asm


def main():
    with open("code.vsl", "r") as file:
        code = file.read()


    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse_function()
    gen = CodeGen(0)
    assembly = gen.generate(ast)
    print("\n".join(assembly))


main()
