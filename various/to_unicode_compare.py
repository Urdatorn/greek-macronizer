def compare_files(file_path1, file_path2):
    with open(file_path1, 'r', encoding='utf-8') as file1:
        file1_lines = set(file1.readlines())
    
    with open(file_path2, 'r', encoding='utf-8') as file2:
        file2_lines = set(file2.readlines())
    
    # Find differences
    differences = file1_lines.symmetric_difference(file2_lines)
    num_differences = len(differences)
    
    if num_differences > 0:
        print("Differing lines:")
        for line in differences:
            print(line.strip())
    print(f"Number of differing lines: {num_differences}")

# Example usage
file_path1 = 'tokens/tokens_no_punct.txt'
file_path2 = 'tokens/tokens_no_punct_compare.txt'
compare_files(file_path1, file_path2)
