ifrom sub_domains_hierarchy import subdomains_hierarchy
from graphics import logo  # Import the ASCII art
import dns.resolver
import time

# Print the ASCII art and instructions
print(logo)
print("This script checks for subdomains and nested subdomains based on the provided primary domain.")
print("It stops checking nested subdomains at the first occurrence of an error or non-existent domain.\n")

found_subdomains = []
not_found_subdomains = []

def resolve_subdomain(full_domain, timeout):
    try:
        cname_answers = dns.resolver.resolve(full_domain, 'CNAME', lifetime=timeout)
        cname_record = cname_answers[0].target.to_text()
        found_subdomains.append(f"{full_domain} is an alias (CNAME) for {cname_record}")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        pass
    except Exception as e:
        not_found_subdomains.append(f"{full_domain}: Error occurred while resolving CNAME: {e}")
        return False

    try:
        answers = dns.resolver.resolve(full_domain, 'A', lifetime=timeout)
        ips = [answer.to_text() for answer in answers]
        found_subdomains.append(f"{full_domain} resolves to: {', '.join(ips)}")
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        not_found_subdomains.append(f"{full_domain} does not exist or has no A records.")
    except Exception as e:
        not_found_subdomains.append(f"{full_domain}: Error occurred while resolving A record: {e}")
    
    return False

def resolve_and_follow_subdomain(initial_subdomain, nested_subdomains, primary_domain, timeout):
    initial_full_domain = f"{initial_subdomain}.{primary_domain}"
    found = resolve_subdomain(initial_full_domain, timeout)
    index = 0

    while found and nested_subdomains and index < len(nested_subdomains):
        subdomain = nested_subdomains[index]
        full_domain = f"{subdomain}.{primary_domain}"
        found = resolve_subdomain(full_domain, timeout)
        index += 1

RATE_LIMIT_SECONDS = 3
TIMEOUT_SECONDS = 8

primary_domain = input("Enter the primary domain: ")

for initial_subdomain, nested_subdomains in subdomains_hierarchy.items():
    resolve_and_follow_subdomain(initial_subdomain, nested_subdomains or [], primary_domain, TIMEOUT_SECONDS)
    time.sleep(RATE_LIMIT_SECONDS)

# Output the results
if found_subdomains:
    print("\nSubdomains Found:")
    for subdomain in found_subdomains:
        print(subdomain)

if not_found_subdomains:
    print("\nRecords Not Found:")
    for subdomain in not_found_subdomains:
        print(subdomain)

