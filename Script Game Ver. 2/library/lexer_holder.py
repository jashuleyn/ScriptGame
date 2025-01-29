import re


#######################################
# CONSTANTS
#######################################


DIGITS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_DIGITS = LETTERS + DIGITS


#######################################
# TOKENS
#######################################


TT_INT          = 'num INT'
TT_FLOAT        = 'float FLOAT'
TT_DOUBLE       = 'double DOUBLE'
TT_IDENTIFIER   = 'IDENTIFIER'
TT_KEYWORD      = 'KEYWORD'
TT_STRING       = 'text STRING'
TT_OPERATOR     = 'OPERATOR'
TT_DELIMITER    = 'DELIMITER'
TT_COMMENT      = 'COMMENT'
TT_SINGLE_COMMENT = 'SINGLE COMMENT'
TT_MULTI_COMMENT  = 'MULTI LINE COMMENT'
TT_EOF          = 'EOF'
TT_BOOLEAN      = 'truth BOOLEAN'
TT_ERROR        = 'ERROR'
TT_REPETITION_ERROR = 'REPETITION ERROR'


KEYWORDS = [
    'greenLight', 'dialogue', 'reveal', 'mingle', 'eliminated', 'teamUp',
    'resetGame', 'num', 'text', 'truth', 'float', 'double',
    'dalgona', 'dalgonaCarve', 'guardSetTime', 'throwWarning', 'throwError',
    'true', 'false', 'break', 'nextGame', 'square', 'triangle', 'circle',
    'deadline', 'warning', 'error', 'area', 'perimeter', 'circumference',
    'diagonal', 'hypotenuse', 'radius','base', 'height', 'array'
]


RESERVED_WORDS = [
    'true', 'false', 'break', 'nextGame', 'square', 'triangle', 'circle', 'deadline', 'warning', 'error'
]

OPERATORS = {
    '=': 'ASSIGNMENTOPERATOR_EQUAL',
    '+=': 'ASSIGNMENTOPERATOR_ADDEQUAL',
    '-=': 'ASSIGNMENTOPERATOR_MINUSEQUAL',
    '*=': 'ASSIGNMENTOPERATOR_MULTIPLYEQUAL',
    '/=': 'ASSIGNMENTOPERATOR_DIVIDEEQUAL',
    '%=': 'ASSIGNMENTOPERATOR_MODULOEQUAL',
    '^=': 'ASSIGNMENTOPERATOR_PORTENTIALEQUAL',
    
    '+': 'UNARYOPERATOR_POSITIVE',
    '-': 'UNARYOPERATOR_NEGATIVE',
    '++': 'UNARYOPERATOR_INCREMENT',
    '--': 'UNARYOPERATOR_DECREMENT',
    
    '&': 'BOOLEANOPERATOR_BITWISEAND',
    '|': 'BOOLEANOPERATOR_BITWISEOR',
    '&&': 'BOOLEANOPERATOR_LOGICALAND',
    '||': 'BOOLEANOPERATOR_LOGICALOR',
    '!': 'BOOLEANOPERATOR_NEGATE',
    
    '>': 'RELATIONALOPERATOR_GREATERTHAN',
    '<': 'RELATIONALOPERATOR_LESSTHAN',
    '==': 'RELATIONALOPERATOR_EQUALEQUAL',
    '!=': 'RELATIONALOPERATOR_NOTEQUAL',
    '>=': 'RELATIONALOPERATOR_GREATERTHANEQUAL',
    '<=': 'RELATIONALOPERATOR_LESSTHANEQUAL',
    
    '+': 'ARITHMETICOPERATOR_ADD',
    '-': 'ARITHMETICOPERATOR_MINUS',
    '*': 'ARITHMETICOPERATOR_MULTIPLY',
    '/': 'ARITHMETICOPERATOR_DIVIDE',
    '%': 'ARITHMETICOPERATOR_MODULO',
    '^': 'ARITHMETICOPERATOR_EXPONENT'
}

DELIMITERS = ['(', ')', '{', '}', ';', ',', ':', '"', '[', ']', '.']

#######################################
# POSITION
#######################################


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt


    def advance(self, current_char):
        self.idx += 1
        self.col += 1


        if current_char == '\n':
            self.ln += 1
            self.col = 0


        return self


    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#######################################
# ERRORS
#######################################


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details


    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


#######################################
# TOKENS CLASS
#######################################


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value


    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


#######################################
# LEXER
#######################################


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()


    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None


    def make_tokens(self):
        tokens = []


        while self.current_char is not None:
            if self.current_char in ' \t':  # Skip spaces and tabs
                self.advance()
            elif self.current_char == '\n':  # Skip newline characters
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                result = self.make_identifier_or_reserved()
                if isinstance(result, Error):
                    return [], result  # Return error immediately
                tokens.append(result)
            elif self.current_char == '/' and self.peek() == '/':
                tokens.append(self.make_single_comment())
            elif self.current_char == '/' and self.peek() == '*':
                tokens.append(self.make_multi_comment())
            elif self.current_char == '"':  # Handle string literals
                tokens.append(self.make_text_string())
            elif self.current_char in OPERATORS:
                tokens.append(self.make_operator())  # Operators handled properly now
            elif self.check_repetition():  # Check for 3+ repeated symbols before processing
                tokens.append(self.make_repetition_error())
                return tokens, Error(self.pos, self.pos, "Repetition Error", "Three or more repeated symbols detected")
            elif self.current_char in DELIMITERS:
                tokens.append(self.make_delimiter())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, ';'))  # Add EOF token
        return tokens, None


    def make_number(self):
        num_str = ''
        dot_count = 0


        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()


        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


    def make_identifier_or_reserved(self):
        id_str = ''
        pos_start = self.pos.copy()


        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()


        # Handle reserved words
        if id_str in RESERVED_WORDS:
            if id_str in ['true', 'false']:  # Special handling for truth BOOLEAN
                return Token(TT_BOOLEAN, id_str)  # Token type is 'truth BOOLEAN'
            return Token(TT_KEYWORD, id_str)


        # Recognize keywords
        if id_str in KEYWORDS:
            return Token(TT_KEYWORD, id_str)


        # Recognize identifiers
        if id_str[0] in LETTERS:
            return Token(TT_IDENTIFIER, id_str)


        # If it doesn't start with a letter, it's invalid
        return IllegalCharError(pos_start, self.pos, f"Illegal identifier: {id_str}")


    def make_text_string(self):
        string = ''
        self.advance()  # Skip the opening "


        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.advance()


        if self.current_char == '"':  # Closing "
            self.advance()
            return Token(TT_STRING, f'"{string}"')  # Include quotes in the token value
        else:
            # Handle error for unmatched quotes
            pos_start = self.pos.copy()
            return IllegalCharError(pos_start, self.pos, "Unmatched double quote")


    def make_operator(self):
        pos_start = self.pos.copy()
        op_str = self.current_char
        self.advance()

        # Handle two-character operators first (++, --, ==, etc.)
        if self.current_char and (op_str + self.current_char) in OPERATORS:
            op_str += self.current_char
            self.advance()

            # Ensure that we are NOT treating "a++" or "b++" as an error
            if not self.check_repetition():
                return Token(OPERATORS.get(op_str, TT_OPERATOR), op_str)

        # If we detect 3+ repeated symbols, handle as repetition error
        if self.check_repetition():
            return self.make_repetition_error()

        return Token(OPERATORS.get(op_str, TT_OPERATOR), op_str)

    def make_single_comment(self):
        comment = ''
        self.advance()  # Skip the first '/'
        self.advance()  # Skip the second '/'


        while self.current_char is not None and self.current_char != '\n':  # Until the end of the line
            comment += self.current_char
            self.advance()


        # Treat everything after // as a single comment
        return Token(TT_SINGLE_COMMENT, f"// {comment.strip()}")


    def make_multi_comment(self):
        comment = ''
        self.advance()  # Skip the first '/'
        self.advance()  # Skip the '*'


        while self.current_char is not None:
            if self.current_char == '*' and self.peek() == '/':  # Detect the closing '*/'
                self.advance()  # Skip the '*'
                self.advance()  # Skip the '/'
                break
            comment += self.current_char
            self.advance()


        if self.current_char is None:  # Handle unclosed multi-line comment
            pos_start = self.pos.copy()
            return IllegalCharError(pos_start, self.pos, "Unclosed multi-line comment")


        # Treat everything between /* and */ as a single comment
        return Token(TT_MULTI_COMMENT, f"/* {comment.strip()} */")


    def make_delimiter(self):
        delimiter_map = {
            '(': 'DELIMITER_LPAREN',
            ')': 'DELIMITER_RPAREN',
            '{': 'DELIMITER_LCURLYB',
            '}': 'DELIMITER_RCURLYB',
            '[': 'DELIMITER_LSQUAREB',
            ']': 'DELIMITER_RSQUAREB',
            ',': 'DELIMITER_COMMA',
            ':': 'DELIMITER_COLON',
            ';': 'DELIMITER_SEMICOLON',
            '.': 'DELIMITER_DOT'
        }


        token_type = delimiter_map.get(self.current_char, 'DELIMITER')
        token = Token(token_type, self.current_char)
        self.advance()
        return token
    
    def make_repetition_error(self):
        """Immediately triggers a repetition error when encountering three consecutive symbols."""
        repeated_char = self.current_char
        error_value = self.current_char
        count = 1  # Start with first occurrence

        while self.current_char == repeated_char:
            self.advance()
            if self.current_char == repeated_char:
                error_value += self.current_char
                count += 1
            if count >= 3:  # Immediately return an error when 3+ symbols appear
                return Token(TT_REPETITION_ERROR, error_value)

        return Token(OPERATORS.get(repeated_char, TT_OPERATOR), repeated_char)  # Return normal token if <3


    def check_repetition(self):
        """Returns True if three consecutive characters are identical (for repetition error)."""
        return (
            self.current_char is not None
            and self.pos.idx + 2 < len(self.text)
            and self.text[self.pos.idx] == self.text[self.pos.idx + 1] == self.text[self.pos.idx + 2]
        )
    
    def peek(self):
        if self.pos.idx + 1 >= len(self.text):
            return None
        return self.text[self.pos.idx + 1]




#######################################
# RUN
#######################################


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()


    return tokens, error















