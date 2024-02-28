import csv
from utils import count_dichrona

def count_dichrona_in_file(input_file_path):
    """Count DICHRONA characters in the first column of a tabulated text file."""
    total_dichrona = 0
    with open(input_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row:  # Ensure the row is not empty
                first_column = row[0]
                total_dichrona += count_dichrona(first_column)
    return total_dichrona

#def main():
#    input_file_path = 'your_input_file.txt'  # Change this to your actual input file path
#    total_dichrona = count_dichrona_in_file(input_file_path)
#    print(f"Total DICHRONA characters in the first column: {total_dichrona}")

#if __name__ == "__main__":
#    main()

input_file_path = 'prepare_tokens/tokens/tokens_no_dup.txt'  # Change this to your actual input file path
total_dichrona = count_dichrona_in_file(input_file_path)
print(f"Total DICHRONA characters in the first column: {total_dichrona}")