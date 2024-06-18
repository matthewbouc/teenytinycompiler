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
        self.comparisonOperators = [TokenType.GT, TokenType.GTEQ, TokenType.LT, TokenType.LTEQ, TokenType.EQEQ, TokenType.NOTEQ]

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

        # Skip excess newlines
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

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

        # "WHILE" comparison "REPEAT" nl {STATEMENT nl} "endwhile" nl
            case TokenType.WHILE:
                print("STATEMENT-WHILE")
                self.nextToken()
                self.comparison()

                self.match(TokenType.REPEAT)
                self.newline()

                while not self.checkToken(TokenType.ENDWHILE):
                    self.statement()

                self.match(TokenType.ENDWHILE)

        # "LABEL" ident
            case TokenType.LABEL:
                print("STATEMENT-LABEL")
                self.nextToken()
                self.match(TokenType.IDENT)

        # "GOTO" ident
            case TokenType.GOTO:
                print("STATEMENT-GOTO")
                self.nextToken()
                self.match(TokenType.IDENT)

        # "LET" ident "=" expression
            case TokenType.LET:
                print("STATEMENT-LET")
                self.nextToken()
                self.match(TokenType.IDENT)
                self.match(TokenType.EQ)
                self.expression()

        # "INPUT" ident
            case TokenType.INPUT:
                print("STATEMENT-INPUT")
                self.nextToken()
                self.match(TokenType.IDENT)

            case _:
                self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")
        # end statement


        self.newline()

    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")

        self.expression()

        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text())

        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    def isComparisonOperator(self):
        return self.curToken.kind in self.comparisonOperators

    # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")
        self.term()

        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("TERM")

        self.unary()
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    # primary ::= number | ident
    def primary(self):
        print("PRIMARY ( " + self.curToken.text + " ) ")

        if self.checkToken(TokenType.NUMBER) or self.checkToken(TokenType.IDENT):
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.curToken.text)
