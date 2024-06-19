import sublist3r

def run_sublist3r(domain, output_file):
    # Run Sublist3r to find subdomains
    # savefile=None because sublist3r does not have the right format for pihole blocklists
    subdomains = sublist3r.main(domain, 40, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
    
    # Format the subdomains for pihole blocklists
    formatted_subdomains = [f"0.0.0.0 {subdomain}" for subdomain in subdomains]
    
    # Write the formatted subdomains to the output file
    with open(output_file, 'w') as file:
        for entry in formatted_subdomains:
            file.write(f"{entry}\n")
    
    print(f"Subdomains for {domain} have been written to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python sublist3r_script.py <domain> <output_file>")
    else:
        domain = sys.argv[1]
        output_file = sys.argv[2]
        run_sublist3r(domain, output_file)
