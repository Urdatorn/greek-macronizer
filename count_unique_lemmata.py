# Path to your file
file_path = 'macrons.txt'

# Initialize an empty set to store unique lemmas
unique_lemmas = set()

# Open and read the file
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Split the line by tab and extract the lemma (third element)
        parts = line.strip().split('\t')
        if len(parts) >= 3:  # Check if there are at least 3 columns in this line
            lemma = parts[2]
            # Add the lemma to the set
            unique_lemmas.add(lemma)

# The number of unique lemmas is the size of the set
unique_lemmas_count = len(unique_lemmas)
print(f'The number of unique lemmata is: {unique_lemmas_count}')
