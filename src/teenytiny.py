from Lexer import *
from Token import Token
from TokenType import *
from Parser import *


def main():
    print("Teeny Tiny Compiler\n")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program()
    print("Parsing completed")

    # source = "IF+-123 foo*THEN/"
    # lexer = Lexer(source)
    # token = lexer.getToken()
    # while token.kind != TokenType.EOF:
    #     print(token.kind)
    #     token = lexer.getToken()


main()
