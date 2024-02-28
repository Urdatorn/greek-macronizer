import csv
import argparse

def remove_stars(input_file_path, output_file_path):
    asterisks_removed = 0  # Initialize counter for removed asterisks

    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
            reader = csv.reader(input_file, delimiter='\t')
            writer = csv.writer(output_file, delimiter='\t')
            
            for row in reader:
                if len(row) >= 3:
                    # Count '*' in the first and third columns before removal
                    asterisks_removed += row[0].count('*') + row[2].count('*')

                    # Remove '*' from the first and third columns
                    row[0] = row[0].replace('*', '')
                    row[2] = row[2].replace('*', '')
                    writer.writerow(row)
                else:
                    # Optionally handle rows that don't have three columns
                    print(f"Skipping row due to incorrect format: {row}")

        print(f"Processed file saved to: {output_file_path}")
        print(f"Total asterisks removed: {asterisks_removed}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Remove "*" symbols from the first and third columns of a text file and report the total number of asterisks removed.')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    args = parser.parse_args()

    remove_stars(args.input, args.output)

if __name__ == "__main__":
    main()
