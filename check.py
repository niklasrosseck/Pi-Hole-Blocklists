def read_file_to_list(filepath):
    with open(filepath, 'r') as file:
        return [line.strip().lower().replace('\t', ' ').rstrip('^') for line in file]

def check_entries(file1, file2):
    entries = read_file_to_list(file1)
    target_entries = set(read_file_to_list(file2))

    missing_entries = [entry for entry in entries if entry not in target_entries]

    with open(file2, 'a') as file:
        for entry in missing_entries:
            file.write(f"{entry}\n")

    return missing_entries

def main():
    # The file you want to check in
    file1 = 'Blocklists/SocialMedia/test.txt'
    # The file you want to append with missing entries
    file2 = 'Blocklists/SocialMedia/facebook.txt'

    missing_entries = check_entries(file1, file2)

    for entry in missing_entries:
        print(f"{entry}: Not present in file")
    
    
if __name__ == "__main__":
    main()   