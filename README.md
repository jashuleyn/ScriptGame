# Script Game Lexer

## Overview
The Script Game Lexer is a lexical analyzer for the Script Game programming language. It tokenizes source code into meaningful components, enabling further processing by a parser or interpreter.

---

## Features
- **Keywords**: Supports recognition of keywords like `greenLight`, `dialogue`, `reveal`, `teamUp`, and more.
- **Data Types**: Recognizes `truth` (boolean), `num` (integer), `text` (string), and other types.
- **Operators**: Identifies arithmetic, logical, and comparison operators, such as `+`, `-`, `*`, `/`, `&&`, and `||`.
- **Delimiters**: Recognizes delimiters like `;`, `,`, `()`, `{}`, and `"`.
- **Comments**: Skips single-line comments starting with `//`.
- **Error Handling**: Reports repetition errors, illegal characters, unmatched quotes, and other issues.

---

## File Structure
```
Script Game Lexer/
├── library/
│   └── lexer_holder.py    # Contains the lexer implementation
├── source.sg              # Source code file to analyze
├── symbol_table.sg        # Output file with tokenized results
├── main.py                # Entry point for the lexer
└── README.md              # Documentation (this file)
```

---

## Usage

### Prerequisites
- Python 3.8 or higher

### Running the Lexer
1. Write your Script Game code in the `source.sg` file.
2. Run the lexer by executing the `main.py` script:
   ```bash
   python main.py
   ```
3. The lexical analysis results will be saved in the `symbol_table.sg` file.

---

## Troubleshooting

### Common Errors
- **Repetition Error**: Triggered when an operator or delimiter is repeated unnecessarily (e.g., `/////`, `+++++`).
- **Illegal Character**: Indicates an unsupported or unexpected character.
- **Unmatched Quotes**: Ensures all string literals have both opening and closing quotes.

---

## License
This project is licensed under the MIT License.


