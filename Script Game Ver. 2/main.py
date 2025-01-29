from library.lexer_holder import run

def main():
    # Read the source file
    with open('source.sg', 'r') as source_file:
        code = source_file.read()

    # Run the lexer on the code
    tokens, error = run('source.sg', code)

    # Write the results to symbol_table.sg
    with open('symbol_table.sg', 'w') as symbol_table:
        symbol_table.write(f"TYPE{' ' * 40}VALUE\n")
        symbol_table.write(f"{'-' * 55}\n")

        if error:
            # Log lexer-level errors
            symbol_table.write(f"ERROR{' ' * 33}{error.as_string()}\n")
            print(f"TOKEN (type: ERROR, lexeme: {error.as_string()}, literal: null")
        else:
            for token in tokens:
                if hasattr(token, "type") and hasattr(token, "value"):
                    # Process valid tokens
                    type_spacing = ' ' * (40 - len(token.type))  # Adjust spacing for alignment
                    value = token.value if token.value is not None else 'None'
                    symbol_table.write(f"{token.type}{type_spacing}{value}\n")

                    # Print token in the requested format to the terminal
                    print(f"TOKEN (type: {token.type}, lexeme: {value}, literal: null)")

                else:
                    # Handle unexpected errors or invalid tokens
                    symbol_table.write(f"ERROR{' ' * 33}Invalid token or error encountered: {str(token)}\n")
                    print(f"TOKEN (type: ERROR, lexeme: Invalid token, literal: null")

    print("Lexical analysis complete. Results saved to symbol_table.sg.")

if __name__ == "__main__":
    main()
