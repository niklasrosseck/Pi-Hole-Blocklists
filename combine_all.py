# A script to combine all blocklists together
# It is also possible to exclude specified subdirectories to construct individual blocklists

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

def combine_all_blocklists(directory, output_file, exclude_subdirectories):
    # Use a dictionary to include headers for blocklists
    combined_entries = {}
    
    # Read all blocklist files from the given directory and add them to the combined entries dictionary
    for root, dirs, files in os.walk(directory):
        # Exclude specified directories
        for exclude_dir in exclude_subdirectories:
            if exclude_dir in dirs:
                dirs.remove(exclude_dir)

        for file in files:
            # Only read blocklist files
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                print(f"Reading blocklist from {filepath}")
                entries = read_blocklist(filepath)
                combined_entries[filepath] = entries

    write_blocklist(output_file, combined_entries)

def main():
    # Directory to search for blocklist files
    directory = 'Blocklists'
    # Output file for the combined blocklist
    output_file = 'Blocklists/CombinedLists/combined_all.txt'
    # Exclude subdiretories for allowing to combine single subdiretories
    exclude_subdirectories = ['CombinedLists']

    combine_all_blocklists(directory, output_file, exclude_subdirectories)
    print(f"Combined blocklist written to {output_file}")

if __name__ == "__main__":
    main()
