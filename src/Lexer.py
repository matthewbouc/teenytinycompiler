import sys
from Token import *
from TokenType import *


class Lexer:
    def __init__(self, source):
        self.source = source + '\n'
        self.curChar = ''
        self.curPos = -1
        self.nextChar()

    # Process the next character or declare EOF (end of file)
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'
        else:
            self.curChar = self.source[self.curPos]

    # Look at and return the next character without updating current position
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]
    
    def abort(self, message):
        sys.exit("lexing error. " + message)

    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    def skipComment(self):
        pass

    def getToken(self):
        self.skipWhitespace()

        match self.curChar:
            case '+':
                token = Token(self.curChar, TokenType.PLUS)
            case '-':
                token = Token(self.curChar, TokenType.MINUS)
            case '*':
                token = Token(self.curChar, TokenType.ASTERISK)
            case '/':
                token = Token(self.curChar, TokenType.SLASH)
            case '\n':
                token = Token(self.curChar, TokenType.NEWLINE)
            case '\0':
                token = Token('', TokenType.EOF)
            case _:
                self.abort("unknown token: " + self.curChar)

        self.nextChar()
        return token