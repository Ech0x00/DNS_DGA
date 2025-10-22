import random
import datetime
import hashlib
import argparse

ch = "abcdefghijklmnopqrstuvwxyz0123456789"
tld = [".com", ".net", ".org", ".biz", ".info"]

def gen_domains(seed, num):
    doms = []
    for _ in range(num):
        dl = random.randint(12, 20)
        d = ""
        for _ in range(dl):
            d += random.choice(ch)
        d += random.choice(tld)
        doms.append(d)
    return doms

def dga(y, m, d):
    seed = hashlib.md5(f"{y}{m}{d}".encode()).hexdigest()
    random.seed(seed)
    num = random.randint(1000, 5000)
    doms = gen_domains(seed, num)
    return doms

def gen_past(days=1):
    now = datetime.datetime.now()
    doms = []
    for i in range(days):
        pd = now - datetime.timedelta(days=i)
        doms.extend(dga(pd.year, pd.month, pd.day))
    return doms

def main():
    p = argparse.ArgumentParser(description='Generate Dyre DGA domains and save to file')
    p.add_argument('--days', type=int, default=1, help='Number of past days')
    p.add_argument('--output', type=str, default='dga_domains.txt', help='Output file')
    args = p.parse_args()
    doms = gen_past(args.days)
    with open(args.output, 'w') as f:
        for d in doms:
            f.write(d + '\n')
    print(f"Generated {len(doms)} DGA domains and saved to {args.output}")

if __name__ == "__main__":
    main()		
