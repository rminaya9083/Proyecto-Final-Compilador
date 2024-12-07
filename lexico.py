import re

especificacionesTokens = [
    ('Number', r'\d+(\.\d*)?'),                             # Detectamos números enteros o decimales
    ('Keyword', r'\b(if|else|elif|while|for|return|int|float|string)\b'),  # Detectamos las palabras reservadas
    ('Identifier', r'[A-Za-z_]\w*'),                        # Detectamos los identificadores
    ('Operator', r'[+\-*/]'),                               # Detectamos los operadores
    ('Logical', r'(==|!=|<=|>=|<|>|&&|\|\|)'),              # Detectamos los operadores lógicos
    ('Assignment', r'='),                                   # Detectamos el operador de asignación
    ('String', r'\".*?\"|\'.*?\''),                         # Detectamos literales de cadena
    ('Comment', r'//.*|/\*[\s\S]*?\*/'),                    # Detectamos comentarios
    ('Skip', r'[ \t\n]+'),                                  # Espacios en blanco (ignorar)
    ('Other', r'.'),                                        # Otros caracteres
]

delimitadores = {'(': 'Delimiter', ')': 'Delimiter', '[': 'Delimiter', ']': 'Delimiter', '{': 'Delimiter', '}': 'Delimiter', ';': 'Delimiter', ':': 'Delimiter', ',': 'Delimiter'}

def lexer(code):
    tokens = []
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in especificacionesTokens)
    pos = 0
    while pos < len(code):
        match = re.match(tok_regex, code[pos:])
        if match:
            kind = match.lastgroup
            value = match.group()
            if kind == 'Skip' or kind == 'Other':
                pos += len(value)
                continue
            tokens.append((kind, value))
            pos += len(value)
        elif code[pos] in delimitadores:
            tokens.append((delimitadores[code[pos]], code[pos]))
            pos += 1
        else:
            raise RuntimeError(f'Unexpected character: {code[pos]!r} at position {pos}')
    return tokens