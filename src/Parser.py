import sys
from Lexer import *

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, Lexer):
        self.lexer = Lexer
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken() # Call twice to initialize both curToken and peekToken.

    def checkToken(self, kind):
        return kind == self.curToken.kind

    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error: " + message)

    def newline(self):
        print("NEWLINE")

        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()


#### Production Rules ####

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # Parse all statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

    # statement ::= ....
    def statement(self):
        match self.curToken.kind:
        # "PRINT" (expression | string) nl
            case TokenType.PRINT:
                print("STATEMENT-PRINT")
                self.nextToken()

                if self.checkToken(TokenType.STRING):
                    # Simple string
                    self.nextToken()
                else:
                    # Expect an expression
                    self.expression()
        # "IF" comparison "THEN" {statement} "ENDIF"
            case TokenType.IF:
                print("STATEMENT-IF")
                self.nextToken()
                self.comparison() # TODO build this out

                self.match(TokenType.THEN)
                self.newline()

                # zero or more statements in the body
                while not self.checkToken(TokenType.ENDIF):
                    self.statement()

                self.match(TokenType.ENDIF)




            case _:
                self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")
        # end statement
        self.newline()
