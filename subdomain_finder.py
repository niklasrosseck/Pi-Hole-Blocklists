import sublist3r

def run_sublist3r(domain, output_file):
    # Run Sublist3r to find subdomains
    # savefile=None because sublist3r does not have the right format for pihole blocklists
    subdomains = sublist3r.main(domain, 40, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
    
    # Format the subdomains for blocklists
    formatted_subdomains = [f"0.0.0.0 {subdomain}" for subdomain in subdomains]
    
    # Write the formatted subdomains to the output file
    with open(output_file, 'w') as file:
        for entry in formatted_subdomains:
            file.write(f"{entry}\n")
    
    print(f"Subdomains for {domain} have been written to {output_file}")

def main():
    # Specify the domain
    domain = 'netflix.com'
    output_file = f'Subdomains/{domain}.txt'
    
    run_sublist3r(domain, output_file)

if __name__ == "__main__":
    main()



