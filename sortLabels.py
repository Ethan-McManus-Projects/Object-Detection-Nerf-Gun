import re
import pandas as pd
import argparse

def natural_sort_key(s):
    """Sort strings in a way that humans expect."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def sort_csv(csv_path):
    # Read the CSV file, skipping the first line
    df = pd.read_csv(csv_path, skiprows=1, header=None)
    # Sort the DataFrame based on the first column using natural sorting
    df = df.sort_values(by=0, key=lambda col: col.map(natural_sort_key))
    # Read the first line separately
    with open(csv_path, 'r') as file:
        first_line = file.readline().strip()
    # Save the sorted DataFrame back to the CSV file, preserving the first line
    with open(csv_path, 'w') as file:
        file.write(first_line + '\n')
        df.to_csv(file, header=False, index=False)

def remove_blank_lines(csv_path):
    # Read the CSV file
    with open(csv_path, 'r') as file:
        lines = file.readlines()
    # Remove blank lines
    lines = [line for line in lines if line.strip()]
    # Write the cleaned lines back to the CSV file
    with open(csv_path, 'w') as file:
        file.writelines(lines)

def main():
    parser = argparse.ArgumentParser(description="Sort CSV file based on the first column and remove blank lines.")
    parser.add_argument('--csv_path', type=str, required=True, help='Path to the CSV file')
    args = parser.parse_args()
    sort_csv(args.csv_path)
    remove_blank_lines(args.csv_path)

if __name__ == '__main__':
    main()