#!/usr/bin/env python3
"""
dns_query.py

Read the embedded newline-separated domain list in this file and perform DNS lookups
for each domain sequentially. Prints A/AAAA/CNAME/TXT results per domain.

Usage:
  python dns_query.py --limit 100 --timeout 3 --retries 1 --type A

This file replaces the previous plain list of domains with an executable script
that still contains the domain list embedded below (after __DATA__ marker).
"""

import argparse
import sys
import time
from typing import List

try:
	import dns.resolver
except Exception:
	print("Missing dependency 'dnspython'. Install with: pip install dnspython")
	raise


def load_domains_from_file(path: str) -> List[str]:
	"""Load domains from a newline-separated file."""
	domains: List[str] = []
	with open(path, 'r', encoding='utf-8') as f:
		for line in f:
			d = line.strip()
			if d and not d.startswith('#'):
				domains.append(d)
	return domains


def query_domain(resolver: dns.resolver.Resolver, domain: str, rtype: str, timeout: float, retries: int):
	"""Query a single domain for rtype with timeout and retries.

	Returns a tuple (success: bool, details: str)
	"""
	attempt = 0
	last_err = None
	while attempt <= retries:
		try:
			resolver.lifetime = timeout
			answer = resolver.resolve(domain, rtype)
			return True, ', '.join([r.to_text() for r in answer])
		except Exception as e:
			last_err = e
			attempt += 1
			time.sleep(0.1)
	return False, str(last_err)


def main():
	p = argparse.ArgumentParser(description='Sequential DNS queries for embedded domain list')
	p.add_argument('--limit', type=int, default=0, help='If >0, only process this many domains')
	p.add_argument('--timeout', type=float, default=2.0, help='Timeout (seconds) per DNS query')
	p.add_argument('--retries', type=int, default=0, help='Number of retries on failure')
	p.add_argument('--type', dest='rtype', default='A', choices=['A', 'AAAA', 'CNAME', 'TXT'], help='Record type to query')
	p.add_argument('--nameserver', default=None, help='Optional DNS nameserver (IP) to use')
	# require explicit domain file to avoid hidden hardcoded defaults
	p.add_argument('-f', '--file', dest='file', required=True, help='Path to newline-separated domain file')
	args = p.parse_args()

	# require explicit domain file path
	domains_file = args.file
	try:
		domains = load_domains_from_file(domains_file)
	except FileNotFoundError:
		print(f'No domain file found at {domains_file}. Provide a valid -f/--file path.')
		sys.exit(1)
	if not domains:
		print('No domains found in the script after __DATA__ marker.')
		sys.exit(1)

	if args.limit > 0:
		domains = domains[:args.limit]

	resolver = dns.resolver.Resolver()
	if args.nameserver:
		resolver.nameservers = [args.nameserver]

	print(f'Querying {len(domains)} domains sequentially (type={args.rtype}, timeout={args.timeout}s, retries={args.retries})')

	for idx, d in enumerate(domains, start=1):
		start = time.time()
		ok, details = query_domain(resolver, d, args.rtype, args.timeout, args.retries)
		elapsed = time.time() - start
		status = 'OK' if ok else 'FAIL'
		print(f'[{idx}/{len(domains)}] {d} {status} ({elapsed:.2f}s): {details}')


if __name__ == '__main__':
	main()
