import subprocess
import sys
import os

def find_blocklist_file(domain, root_directory='Blocklists'):
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == domain:
                return os.path.join(dirpath, filename)
    
    # If the blocklist file does not exist, create a new one
    new_blocklist_path = os.path.join(root_directory, domain)
    if not os.path.exists(new_blocklist_path):
        with open(new_blocklist_path, 'w') as f:
            f.write("# Blocklist for {}\n".format(domain))
        return new_blocklist_path
    
    return None

def automate_process(domain, blocklist_file):
    # Find or create the blocklist file path
    blocklist_file = find_blocklist_file(blocklist_file)
    
    # Temporary file for Sublist3r output
    temp_sublist_file = 'temp_subdomains.txt'
    
    # Step 1: Run Sublist3r script
    subprocess.run(['python', 'automate_subdomain_finder.py', domain, temp_sublist_file])

    # Step 2: Run check script to add new entries to blocklist
    subprocess.run(['python', 'automate_check.py', temp_sublist_file, blocklist_file])

    # Clean up the temporary file
    if os.path.exists(temp_sublist_file):
        os.remove(temp_sublist_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python automation.py <domain> <blocklist_file>")
    else:
        domain = sys.argv[1]
        blocklist_file = sys.argv[2]
        automate_process(domain, blocklist_file)
