from Lexer import *
from Token import Token
from TokenType import *


def main():
    # source = "LET foobar = 123"
    # lexer = Lexer(source)
    # while lexer.peek() != '\0':
    #     print(lexer.curChar)
    #     lexer.nextChar()

    source = "+- */"
    lexer = Lexer(source)
    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()

main()
