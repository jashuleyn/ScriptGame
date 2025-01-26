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

### Example Input (`source.sg`):
```plaintext
truth isRaining = true;
truth isCold = true;
truth isWindy = false;

greenLight (isRaining) {
    reveal("It's raining. Take an umbrella.");

    greenLight (isCold) {
        reveal("It's also cold. Wear a jacket.");
    }
    teamUp(isWindy) {
        reveal("And it's windy. Be careful outside!");
    } else {
        reveal("Unknown weather, but it’s raining");
    }
} else {
    reveal("It's not raining. Enjoy the weather!");
}
```

### Expected Output (`symbol_table.sg`):
```plaintext
TYPE                           VALUE
-------------------------------------
KEYWORD                        truth
IDENTIFIER                     isRaining
OPERATOR                       =
truth BOOLEAN                  true
DELIMITER                      ;
KEYWORD                        truth
IDENTIFIER                     isCold
OPERATOR                       =
truth BOOLEAN                  true
DELIMITER                      ;
KEYWORD                        truth
IDENTIFIER                     isWindy
OPERATOR                       =
truth BOOLEAN                  false
DELIMITER                      ;
KEYWORD                        greenLight
DELIMITER                      (
IDENTIFIER                     isRaining
DELIMITER                      )
DELIMITER                      {
KEYWORD                        reveal
DELIMITER                      (
text STRING                    "It's raining. Take an umbrella."
DELIMITER                      )
DELIMITER                      ;
KEYWORD                        greenLight
DELIMITER                      (
IDENTIFIER                     isCold
DELIMITER                      )
DELIMITER                      {
KEYWORD                        reveal
DELIMITER                      (
text STRING                    "It's also cold. Wear a jacket."
DELIMITER                      )
DELIMITER                      ;
DELIMITER                      }
KEYWORD                        teamUp
DELIMITER                      (
IDENTIFIER                     isWindy
DELIMITER                      )
DELIMITER                      {
KEYWORD                        reveal
DELIMITER                      (
text STRING                    "And it's windy. Be careful outside!"
DELIMITER                      )
DELIMITER                      ;
DELIMITER                      }
KEYWORD                        else
DELIMITER                      {
KEYWORD                        reveal
DELIMITER                      (
text STRING                    "Unknown weather, but it’s raining"
DELIMITER                      )
DELIMITER                      ;
DELIMITER                      }
DELIMITER                      }
KEYWORD                        else
DELIMITER                      {
KEYWORD                        reveal
DELIMITER                      (
text STRING                    "It's not raining. Enjoy the weather!"
DELIMITER                      )
DELIMITER                      ;
DELIMITER                      }
EOF                            ;
```

---

## Troubleshooting
### UnicodeDecodeError
If you encounter a `UnicodeDecodeError`, ensure that `source.sg` uses UTF-8 encoding. Save the file with UTF-8 encoding in your text editor or IDE.

### Common Errors
- **Repetition Error**: Triggered when an operator or delimiter is repeated unnecessarily (e.g., `/////`, `+++++`).
- **Illegal Character**: Indicates an unsupported or unexpected character.
- **Unmatched Quotes**: Ensures all string literals have both opening and closing quotes.

---

## Contributions
Feel free to fork this repository and submit pull requests for improvements or bug fixes.

---

## License
This project is licensed under the MIT License.


