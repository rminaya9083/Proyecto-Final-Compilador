class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class FunctionNode(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForNode(ASTNode):
    def __init__(self, target, iter, body):
        self.target = target
        self.iter = iter
        self.body = body

class BinaryOperationNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

class AssignmentNode(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

def ast_to_string(node, indent=""):
    if isinstance(node, ProgramNode):
        result = f"{indent}ProgramNode\n"
        for stmt in node.statements:
            result += f"{ast_to_string(stmt, indent + '  ')}\n"
        return result.strip()
    elif isinstance(node, FunctionNode):
        result = f"{indent}FunctionNode({node.name})\n"
        result += f"{indent}  Parameters: {', '.join(node.parameters)}\n"
        result += f"{indent}  Body:\n{ast_to_string(node.body, indent + '    ')}"
        return result
    elif isinstance(node, IfNode):
        result = f"{indent}IfNode\n"
        result += f"{indent}  Condition:\n{ast_to_string(node.condition, indent + '    ')}\n"
        result += f"{indent}  Then:\n{ast_to_string(node.then_branch, indent + '    ')}"
        if node.else_branch:
            result += f"\n{indent}  Else:\n{ast_to_string(node.else_branch, indent + '    ')}"
        return result
    elif isinstance(node, WhileNode):
        result = f"{indent}WhileNode\n"
        result += f"{indent}  Condition:\n{ast_to_string(node.condition, indent + '    ')}\n"
        result += f"{indent}  Body:\n{ast_to_string(node.body, indent + '    ')}"
        return result
    elif isinstance(node, ForNode):
        result = f"{indent}ForNode\n"
        result += f"{indent}  Target: {ast_to_string(node.target, indent + '  ')}\n"
        result += f"{indent}  Iter: {ast_to_string(node.iter, indent + '  ')}\n"
        result += f"{indent}  Body:\n{ast_to_string(node.body, indent + '    ')}"
        return result
    elif isinstance(node, BinaryOperationNode):
        return f"{indent}BinaryOperationNode({node.operator})\n" \
               f"{ast_to_string(node.left, indent + '  ')}\n" \
               f"{ast_to_string(node.right, indent + '  ')}"
    elif isinstance(node, NumberNode):
        return f"{indent}NumberNode({node.value})"
    elif isinstance(node, IdentifierNode):
        return f"{indent}IdentifierNode({node.name})"
    elif isinstance(node, AssignmentNode):
        result = f"{indent}AssignmentNode\n"
        result += f"{indent}  Identifier: {node.identifier}\n"
        result += f"{indent}  Expression:\n{ast_to_string(node.expression, indent + '    ')}"
        return result
    else:
        return f"{indent}UnknownNode"
