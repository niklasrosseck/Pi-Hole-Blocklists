# A script to combine specified blocklists to create a unique blocklist

import os

def read_blocklist(filepath):
    with open(filepath, 'r') as file:
        # File should already be normalized but just to make sure it gets normalized again
        return {line.strip().lower().replace('\t', ' ').rstrip('^') for line in file if line.strip() and not line.startswith('#')}

def write_blocklist(filepath, entries_dict):
    # Write the combined blocklist to the given output file
    with open(filepath, 'w') as file:
        # Add a header for the combined blocklist
        file.write("# Combined block list\n\n")
        # Sort the entries by header and write them to the output file
        for header, entries in entries_dict.items():
            file.write(f"# Blocklist from {header}\n\n")
            for entry in sorted(entries):
                file.write(f"{entry}\n")
            file.write("\n")

def combine_selected_blocklists(directory, selected_files, output_file):
    # Use a dictionary to include headers for blocklists
    combined_entries = {}
    
    # Goes through the directory and finds selected files
    for root, _, files in os.walk(directory):
        for file in files:
            if file in selected_files:
                filepath = os.path.join(root, file)
                print(f"Reading blocklist from {filepath}")
                entries = read_blocklist(filepath)
                combined_entries[filepath] = entries

    write_blocklist(output_file, combined_entries)

def main():
    # Directory to search for blocklist files
    directory = 'Blocklists'
    # Output file for the combined blocklist
    output_file = 'combined_selected.txt'
    
    # Print the available blocklist files to make it easier for the user
    print("Available blocklist files:")
    available_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                print(file)
                available_files.append(file)

    selected_files = input("\nEnter the names of the files you want to combine, separated by commas:\n").split(',')

    selected_files = [file.strip() for file in selected_files]

    # Check if the entered files exist
    valid_files = [file for file in selected_files if file in available_files]

    if not valid_files:
        print("No valid files selected. Exiting.")
        return

    combine_selected_blocklists(directory, valid_files, output_file)
    print(f"Combined blocklist written to {output_file}")

if __name__ == "__main__":
    main()
