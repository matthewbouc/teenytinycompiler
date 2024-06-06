from Lexer import *
from Token import Token
from TokenType import *


def main():

    source = "IF+-123 foo*THEN/"
    lexer = Lexer(source)
    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()


main()
