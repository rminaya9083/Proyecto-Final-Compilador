from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        statements = []
        while self.peek():
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.peek()
        if token[0] == 'Keyword':
            if token[1] == 'if':
                return self.parse_if_statement()
            elif token[1] == 'while':
                return self.parse_while_statement()
            elif token[1] == 'for':
                return self.parse_for_statement()
            elif token[1] == 'def':
                return self.parse_function_definition()
            elif token[1] == 'return':
                return self.parse_return_statement()
        elif token[0] == 'Identifier':
            return self.parse_assignment_or_expression()
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_if_statement(self):
        self.consume('Keyword', 'if')
        condition = self.parse_expression()
        self.consume('Delimiter', '{')
        then_branch = self.parse_block()
        self.consume('Delimiter', '}')
        else_branch = None
        if self.peek() and self.peek()[0] == 'Keyword' and self.peek()[1] == 'else':
            self.consume('Keyword', 'else')
            self.consume('Delimiter', '{')
            else_branch = self.parse_block()
            self.consume('Delimiter', '}')
        return IfNode(condition, then_branch, else_branch)

    def parse_while_statement(self):
        self.consume('Keyword', 'while')
        condition = self.parse_expression()
        self.consume('Delimiter', '{')
        body = self.parse_block()
        self.consume('Delimiter', '}')
        return WhileNode(condition, body)

    def parse_for_statement(self):
        self.consume('Keyword', 'for')
        identifier = self.consume('Identifier')[1]
        self.consume('Keyword', 'in')
        iterable = self.parse_expression()
        self.consume('Delimiter', '{')
        body = self.parse_block()
        self.consume('Delimiter', '}')
        return ForNode(identifier, iterable, body)

    def parse_function_definition(self):
        self.consume('Keyword', 'def')
        name = self.consume('Identifier')[1]
        self.consume('Delimiter', '(')
        parameters = []
        if self.peek() and self.peek()[0] == 'Identifier':
            parameters.append(self.consume('Identifier')[1])
            while self.peek() and self.peek()[0] == 'Delimiter' and self.peek()[1] == ',':
                self.consume('Delimiter', ',')
                parameters.append(self.consume('Identifier')[1])
        self.consume('Delimiter', ')')
        self.consume('Delimiter', '{')
        body = self.parse_block()
        self.consume('Delimiter', '}')
        return FunctionNode(name, parameters, body)

    def parse_return_statement(self):
        self.consume('Keyword', 'return')
        expression = self.parse_expression()
        self.consume('Delimiter', ';')
        return ReturnNode(expression)

    def parse_block(self):
        statements = []
        while self.peek() and not (self.peek()[0] == 'Delimiter' and self.peek()[1] == '}'):
            statements.append(self.parse_statement())
        return statements

    def parse_assignment_or_expression(self):
        left = self.consume('Identifier')
        if self.peek() and self.peek()[0] == 'Assignment':
            self.consume('Assignment')
            right = self.parse_expression()
            self.consume('Delimiter', ';')
            return AssignmentNode(left[1], right)
        else:
            return self.parse_expression()

    def parse_expression(self):
        left = self.parse_term()
        while self.peek() and self.peek()[0] == 'Operator' and self.peek()[1] in ('+', '-'):
            operator = self.consume('Operator')[1]
            right = self.parse_term()
            left = BinaryOperationNode(left, operator, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.peek() and self.peek()[0] == 'Operator' and self.peek()[1] in ('*', '/'):
            operator = self.consume('Operator')[1]
            right = self.parse_factor()
            left = BinaryOperationNode(left, operator, right)
        return left

    def parse_factor(self):
        token = self.peek()
        if token[0] == 'Number':
            return NumberNode(self.consume('Number')[1])
        elif token[0] == 'Identifier':
            return IdentifierNode(self.consume('Identifier')[1])
        elif token[0] == 'Delimiter' and token[1] == '(':
            self.consume('Delimiter', '(')
            expression = self.parse_expression()
            self.consume('Delimiter', ')')
            return expression
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def peek(self, offset=0):
        index = self.current_token_index + offset
        if index < len(self.tokens):
            return self.tokens[index]
        return None

    def consume(self, token_type, value=None):
        token = self.tokens[self.current_token_index]
        if token[0] != token_type or (value is not None and token[1] != value):
            raise SyntaxError(f"Unexpected token: {token}")
        self.current_token_index += 1
        return token
