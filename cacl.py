# ----------------------
# 极简四则运算编译器
# ----------------------

# 定义Token类型
from enum import Enum
class TokenType(Enum):
    INTEGER = 'INTEGER'
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    LPAREN = '('
    RPAREN = ')'
    EOF = 'EOF'

# Token类
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

# ----------------------
# 词法分析器（Lexer）
# ----------------------
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS)
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS)
            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL)
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV)
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN)
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN)
            raise Exception(f'Invalid character: {self.current_char}')
        return Token(TokenType.EOF)

# ----------------------
# 递归下降语法分析器（Parser）
# ----------------------
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f'Expected {token_type}, got {self.current_token}')

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return ('INTEGER', token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            raise Exception('Invalid factor')

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            op = self.current_token
            self.eat(op.type)
            node = (op.type, node, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token
            self.eat(op.type)
            node = (op.type, node, self.term())
        return node

# ----------------------
# 中间代码生成器（生成三地址码）
# ----------------------
class CodeGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def new_temp(self):
        self.temp_count += 1
        return f't{self.temp_count}'

    def generate(self, node):
        if node[0] == 'INTEGER':
            return node[1]
        else:
            op, left, right = node
            left_val = self.generate(left)
            right_val = self.generate(right)
            temp = self.new_temp()
            self.code.append(f'{temp} = {left_val} {op} {right_val}')
            return temp

# ----------------------
# 主程序
# ----------------------
if __name__ == '__main__':
    text = '(3 + 5) * 2 - 6 / 3'
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.expr()
    generator = CodeGenerator()
    result = generator.generate(ast)
    print("生成的中间代码:")
    for line in generator.code:
        print(line)
    print(f"最终结果临时变量: {result}")
