## Christopher Guerra
## Program designed to read a file and display a table of the code, tokenized, and total number of tokens in the code.

import os.path
import re

# Change to the file name being used
filename = "TesterFile.txt"

# Define the categories of tokens (keywords, identifiers, operators, delimiters, literals)
categories = {
    "Keywords": ["def", "return", "for", "in", "range", "print", "int", "while", "if", "else", "elif"],
    "Identifiers": ["add", "greet", "a", "b", "result", "count", "i", "number"],
    "Operators": ["=", "+", "-", "++", "--", "+=", "-=", "*", "*=", "/"],
    "Delimiters": ["(", ")", ",", ":", "[", "]", "{", "}", ";"],
    "Literals": []  
}

# Initialize found tokens and total token count
found_tokens = {category: [] for category in categories}  # Store found tokens for each category
total_count = 0  # Initialize total token count

# Regex pattern to match string literals, words, and delimiters
tokens_regex = re.compile(r'\".*?\"|\'.*?\'|\w+|[^\w\s]')  # Matches string literals, words, and symbols

# Check if the file exists
if not os.path.isfile(filename):
    print('File does not exist.')
    exit()

# Read file and split it into lines
with open(filename) as f:
    content = f.read().splitlines()  

# Iterate over each line in the file, removing excess whitespace from the line
for line in content:
    filterLine = line.strip()  

    # Remove comments from the line, and only keep code before comments if on same line
    if '#' in filterLine:
        filterLine = filterLine.split('#')[0].strip()  

    # Skip empty lines after removing comments
    if not filterLine:
        continue

    # Find all string literals in the line
    literal_quotes = re.findall(r'\"(.*?)\"|\'(.*?)\'', filterLine)
    for quote in literal_quotes:
        # Used to handle both double and single quotes
        literal = quote[0] if quote[0] else quote[1]  
        # Add literal to the found tokens list
        if literal not in found_tokens["Literals"]:
            found_tokens["Literals"].append(literal) 
        #Increment total token count
        total_count += 1  

    # Find all tokens in the line (including literals, keywords, identifiers, operators, and delimiters)
    tokens_in_line = re.findall(tokens_regex, filterLine)

    # Iterate over each token found in the line
    for token in tokens_in_line:
        for category, tokens in categories.items():
            # Check if the token belongs to the category or if it's already identified as a literal
            if token in tokens or (category == "Literals" and token in found_tokens[category]):
                if token not in found_tokens[category]:
                    found_tokens[category].append(token)  # Add token to the found tokens list for the category
                total_count += 1  # Increment total token count
                break  # Stop once the token is categorized

# Output the categorized tokens for each category
print("\nCategory     Tokens")
for category, tokens in found_tokens.items():
    token_list = ', '.join(tokens) if tokens else "None"  # Join tokens in a category into a string
    print(f"{category:<12} {token_list}")  # Print category and its tokens

# Print the total token count
print(f"\nToken Total: {total_count}")
