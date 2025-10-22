> Simple Python scripts to simulate Domain Generation Algorithm (DGA) behavior via DNS queries.  

## Overview
**DNS_DGA** is a set of lightweight Python scripts that demonstrates the mechanics behind Domain Generation Algorithms (DGAs) often used in malware communication.  
It generates pseudo-random domain names and can perform DNS lookups against them — useful for blue/purple team exercices.

## Features
- Generate domain names using simple DGA patterns  
- Perform DNS lookups on generated domains  

## Getting Started
```bash
## Clone the repo
git clone https://github.com/Ech0x00/DNS_DGA.git
cd DNS_DGA

### Generate DGA domains
python simple_dga.py --days 1 --output domains.txt

## Query domains with resolver
python dns_query.py -f domains.txt --timeout 3 --retries 1 --type A



