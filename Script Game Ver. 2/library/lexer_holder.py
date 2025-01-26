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
TT_EOF          = 'EOF'
TT_BOOLEAN      = 'truth BOOLEAN'
TT_ERROR        = 'ERROR'

KEYWORDS = [
    'greenLight', 'dialogue', 'reveal', 'mingle', 'eliminated', 'teamUp',
    'resetGame', 'num', 'text', 'truth', 'float', 'double',
    'add', 'remove', 'update', 'enqueue', 'dequeue', 'push', 'pop',
    'insert', 'Array', 'Queue', 'Stack', 'LinkedList',
    'FIFO', 'LIFO', 'fixed-size', 'dynamic', 'singly-linked', 'doubly-linked'
]

OPERATORS = ['+', '-', '*', '/', '%', '^', '=', '+=', '-=', '/=', '%=', '^=', '++', '--', '>', '<', '>=', '<=', '==', '!=', '&&', '||', '!', '.']

DELIMITERS = ['(', ')', '{', '}', ';', ',', ':', '//', '"']

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

class RepetitionError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Repetition Error', details)

#######################################
# TOKENS
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
        repetition_check = ''

        while self.current_char is not None:
            if self.current_char in ' \t':  # Skip spaces and tabs
                self.advance()
            elif self.current_char == '\n':  # Skip newline characters
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                result = self.make_identifier_or_textshape_or_boolean()
                if isinstance(result, Error):
                    return [], result  # Return error immediately
                tokens.append(result)
                repetition_check = ''
            elif self.current_char == '/' and self.peek() == '/':
                tokens.append(Token(TT_DELIMITER, '//'))
                self.skip_comment()
            elif self.current_char == '"':  # Handle string literals
                tokens.append(self.make_text_string())
            elif self.current_char in OPERATORS:
                repetition_check += self.current_char
                if len(set(repetition_check)) == 1 and len(repetition_check) > 2:  # All characters in repetition_check are identical and repeated more than twice
                    pos_start = self.pos.copy()
                    return [], RepetitionError(pos_start, self.pos, f"Repetition Error: Repeated '{self.current_char * len(repetition_check)}' detected")
                tokens.append(Token(TT_OPERATOR, self.current_char))
                self.advance()
            elif self.current_char in DELIMITERS:
                tokens.append(Token(TT_DELIMITER, self.current_char))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, ';'))  # Add EOF token, assigning ';' at end
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

    def make_identifier_or_textshape_or_boolean(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

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

    def peek(self):
        if self.pos.idx + 1 >= len(self.text):
            return None
        return self.text[self.pos.idx + 1]

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error







