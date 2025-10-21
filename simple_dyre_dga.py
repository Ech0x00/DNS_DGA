import random
import datetime
import hashlib

# Define the character sets and top-level domains (TLDs)
chars = "abcdefghijklmnopqrstuvwxyz0123456789"
tlds = [".com", ".net", ".org", ".biz", ".info"]

def generate_domains(seed, num_domains):
    domains = []
    for _ in range(num_domains):
        domain_length = random.randint(12, 20)
        domain = ""
        for _ in range(domain_length):
            domain += random.choice(chars)
        domain += random.choice(tlds)
        domains.append(domain)
    return domains
	
def dyre_dga(year, month, day):
    # Generate a seed value based on the date
    seed = hashlib.md5(f"{year}{month}{day}".encode()).hexdigest()
    random.seed(seed)

    # Generate a list of domains
    num_domains = random.randint(1000, 5000)
    domains = generate_domains(seed, num_domains)

    return domains

def is_dyre_domain(domain, year, month, day):
    dyre_domains = dyre_dga(year, month, day)
    return domain in dyre_domains

def generate_past_dga_domains(days=1):
    current_date = datetime.datetime.now()
    todays_domains = []

    for i in range(days):
        past_date = current_date - datetime.timedelta(days=i)
        todays_domains.extend(dyre_dga(past_date.year, past_date.month, past_date.day))

    return todays_domains

def main():
    current_date = datetime.datetime.now()
    dyre_domains = dyre_dga(current_date.year, current_date.month, current_date.day)

    # Detect a Dyre DGA domain
    dyre_domain = random.choice(dyre_domains)
    print(f"Detecting Dyre DGA domain: {dyre_domain}")
    if is_dyre_domain(dyre_domain, current_date.year, current_date.month, current_date.day):
        print(f"{dyre_domain} is a Dyre DGA domain")
    else:
        print(f"{dyre_domain} is not a Dyre DGA domain")

    # Detect a non-Dyre DGA domain
    non_dyre_domain = "example.com"
    print(f"\nDetecting non-Dyre DGA domain: {non_dyre_domain}")
    if is_dyre_domain(non_dyre_domain, current_date.year, current_date.month, current_date.day):
        print(f"{non_dyre_domain} is a Dyre DGA domain")
    else:
        print(f"{non_dyre_domain} is not a Dyre DGA domain")

    # Generate and print Dyre DGA domains for the past 1 days
    past_dga_domains = generate_past_dga_domains()
    print("\nDyre DGA domains for the past 1 days:")
    for domain in past_dga_domains:
        print(domain)

# @title
if __name__ == "__main__":
    main()		