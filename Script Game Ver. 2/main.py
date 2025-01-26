from library.lexer_holder import run

def main():
    # Read the source file
    with open('source.sg', 'r') as source_file:
        code = source_file.read()

    # Run the lexer on the code
    tokens, error = run('source.sg', code)

    # Write the results to symbol_table.sg
    with open('symbol_table.sg', 'w') as symbol_table:
        if error:
            symbol_table.write(f"TYPE{' ' * 27}VALUE\n")
            symbol_table.write(f"{'-' * 32}\n")
            symbol_table.write(f"ERROR{' ' * 25}{error.as_string()}\n")
        else:
            symbol_table.write(f"TYPE{' ' * 27}VALUE\n")
            symbol_table.write(f"{'-' * 32}\n")
            for token in tokens:
                type_spacing = ' ' * (30 - len(token.type))  # Adjust spacing for alignment
                value = token.value if token.value is not None else 'None'
                symbol_table.write(f"{token.type}{type_spacing}{value}\n")

    print("Lexical analysis complete. Results saved to symbol_table.sg.")

if __name__ == "__main__":
    main()