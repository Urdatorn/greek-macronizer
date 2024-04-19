import sqlite3
import csv

def export_sql_to_tsv(db_path, table_name, output_file_path, macrons_column_index):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to select all entries from the specified table
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    # Fetch all rows from the database
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Write to TSV file, skipping the first column and removing commas from the macrons column
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')

        for row in rows:
            # Skip the first column and sanitize the macrons column by removing commas
            new_row = [item.replace(',', '') if i == macrons_column_index else item for i, item in enumerate(row) if i != 0]
            writer.writerow(new_row)

    print(f"Data successfully written to {output_file_path}")

# Example usage:
db_path = 'crawl_hypotactic/macrons_hypotactic.db'  # Path to the SQLite database
table_name = 'annotated_tokens'  # Table to export
output_file_path = 'macrons_hypotactic.tsv'  # TSV output file path
macrons_column_index = 4  # Index of the 'macrons' column, the fifth column out of five
export_sql_to_tsv(db_path, table_name, output_file_path, macrons_column_index)