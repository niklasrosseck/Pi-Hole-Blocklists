def read_file_to_list(filepath):
    with open(filepath, 'r') as file:
        return [line.strip().lower().replace('\t', ' ').rstrip('^') for line in file]

def check_entries(file1, file2):
    entries = read_file_to_list(file1)
    target_entries = set(read_file_to_list(file2))

    missing_entries = [entry for entry in entries if entry not in target_entries]
    
    # Only appends when there are missing entries
    if missing_entries:
        with open(file2, 'a') as file:
            # Header to better see which domains have been added
            file.write(f"\n\n # Entries added with Sublist3r \n\n")
            for entry in missing_entries:
                file.write(f"{entry}\n")

    return missing_entries

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python check_script.py <file1> <file2>")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        missing_entries = check_entries(file1, file2)
        for entry in missing_entries:
            print(f"{entry}: Not present in file")