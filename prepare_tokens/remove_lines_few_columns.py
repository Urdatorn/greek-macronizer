from utils import Colors

def remove_lines_few_columns(input_file_path, output_file_path, min_columns=3):
    """
    Processes a tab-separated input text file and removes all lines that have fewer than a specified number of columns.
    
    Parameters:
    - input_file_path (str): The path to the input file to be processed.
    - output_file_path (str): The path where the processed file will be saved.
    - min_columns (int): The minimum number of columns required for a line to be retained. Defaults to 3.
    
    Prints the number of removed lines in red and the name of the saved output file path in green. Handles errors related to file reading and writing.
    """
    removed_lines = 0
    try:
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
            lines = input_file.readlines()
            for line in lines:
                if len(line.split('\t')) >= min_columns:
                    output_file.write(line)
                else:
                    removed_lines += 1

        print(f"{Colors.RED}Number of removed lines: {removed_lines}{Colors.ENDC}")
        print(f"{Colors.GREEN}Output saved to: {output_file_path}{Colors.ENDC}")
    except IOError as e:
        print(f"{Colors.RED}An error occurred while processing the file: {e}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}An unexpected error occurred: {e}{Colors.ENDC}")

def main():
    """
    Main function to call the line filtering script with user-specified input and output file paths.
    """
    # Example usage - replace 'input.txt' and 'output.txt' with actual paths as needed
    input_file_path = 'input.txt'
    output_file_path = 'output.txt'
    
    # Call the filtering function
    remove_lines_few_columns(input_file_path, output_file_path)

if __name__ == "__main__":
    main()
