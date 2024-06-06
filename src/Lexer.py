import sys
import re
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
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

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
            case '=':
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.EQEQ)
                else:
                    token = Token(self.curChar, TokenType.EQ)
            case '>':
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.GTEQ)
                else:
                    token = Token(self.curChar, TokenType.GT)
            case '<':
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.LTEQ)
                else:
                    token = Token(self.curChar, TokenType.LT)
            case '!':
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.NOTEQ)
                else:
                    self.abort("Expected !=, got !" + self.peek())
            case '\"':
                self.nextChar()
                startPos = self.curPos
                breakingChars = ['\r', '\n', '\t', '\\', '%']
                while self.curChar != '\"':
                    if self.curChar in breakingChars:
                        self.abort("Illegal character in string.")
                    self.nextChar()
                tokenText = self.source[startPos : self.curPos]
                token = Token(tokenText, TokenType.STRING)

            case _ if self.curChar.isdigit():
                startPos = self.curPos
                while self.peek().isdigit():
                    self.nextChar()
                if self.peek() == '.':
                    self.nextChar()
                    if not self.peek().isdigit():
                        self.abort("Illegal character in number.")
                    while self.peek().isdigit():
                        self.nextChar()
                
                tokenText = self.source[startPos : self.curPos + 1]
                token = Token(tokenText, TokenType.NUMBER)

            case _ if self.curChar.isalpha():
                startPos = self.curPos
                while self.peek().isalnum():
                    self.nextChar()
                tokenText = self.source[startPos : self.curPos + 1]
                keyword = Token.checkIfKeyword(tokenText)
                if keyword == None:
                    token = Token(tokenText, TokenType.IDENT)
                else:
                    token = Token(tokenText, keyword)

            case _:
                self.abort("unknown token: " + self.curChar)

        self.nextChar()
        return token
    