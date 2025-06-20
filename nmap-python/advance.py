#!/usr/bin/env python3
import os
import subprocess
import requests
import json
import socket
import nmap
from theHarvester import theHarvester
from concurrent.futures import ThreadPoolExecutor

# Configuration
TARGET_DOMAIN = "example.com"  # CHANGE TO YOUR TARGET (LEGAL USE ONLY!)
OUTPUT_DIR = "recon_results"
NMAP_ARGS = "-sV -T4"  # Safe timing, version detection
WORDLIST = "/usr/share/wordlists/dirb/common.txt"  # Default Kali wordlist

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def passive_recon():
    """Passive reconnaissance using OSINT tools"""
    print("\n[+] Running passive reconnaissance...")
    
    # 1. WHOIS Lookup
    print("  [*] Performing WHOIS lookup...")
    try:
        whois_result = subprocess.run(["whois", TARGET_DOMAIN], capture_output=True, text=True)
        with open(f"{OUTPUT_DIR}/whois.txt", "w") as f:
            f.write(whois_result.stdout)
    except Exception as e:
        print(f"    [!] WHOIS failed: {e}")

    # 2. theHarvester (emails, subdomains)
    print("  [*] Running theHarvester...")
    try:
        harvester = theHarvester()
        harvester.run_all(TARGET_DOMAIN)
        with open(f"{OUTPUT_DIR}/harvester.txt", "w") as f:
            f.write(str(harvester.get_results()))
    except Exception as e:
        print(f"    [!] theHarvester failed: {e}")

    # 3. DNS Enumeration
    print("  [*] Enumerating DNS records...")
    try:
        dns_records = {}
        record_types = ['A', 'MX', 'TXT', 'NS', 'CNAME']
        for record in record_types:
            result = subprocess.run(["dig", "+short", record, TARGET_DOMAIN], capture_output=True, text=True)
            dns_records[record] = result.stdout.splitlines()
        with open(f"{OUTPUT_DIR}/dns.json", "w") as f:
            json.dump(dns_records, f, indent=4)
    except Exception as e:
        print(f"    [!] DNS enumeration failed: {e}")

def active_recon():
    """Active reconnaissance (requires network access to target)"""
    print("\n[+] Running active reconnaissance...")
    
    # 1. Nmap Scan
    print("  [*] Running Nmap scan...")
    try:
        scanner = nmap.PortScanner()
        scanner.scan(TARGET_DOMAIN, arguments=NMAP_ARGS)
        with open(f"{OUTPUT_DIR}/nmap.txt", "w") as f:
            f.write(json.dumps(scanner.scaninfo(), indent=4))
            for host in scanner.all_hosts():
                f.write(f"\nHost: {host}\n")
                f.write(f"State: {scanner[host].state()}\n")
                for proto in scanner[host].all_protocols():
                    f.write(f"\nProtocol: {proto}\n")
                    ports = scanner[host][proto].keys()
                    for port in ports:
                        f.write(f"Port {port}: {scanner[host][proto][port]['state']} - {scanner[host][proto][port]['name']}\n")
    except Exception as e:
        print(f"    [!] Nmap failed: {e}")

    # 2. Web Directory Brute-forcing
    print("  [*] Running directory brute-forcing...")
    try:
        result = subprocess.run(["gobuster", "dir", "-u", f"http://{TARGET_DOMAIN}", "-w", WORDLIST], 
                              capture_output=True, text=True)
        with open(f"{OUTPUT_DIR}/gobuster.txt", "w") as f:
            f.write(result.stdout)
    except Exception as e:
        print(f"    [!] Gobuster failed: {e}")

    # 3. HTTP Headers Analysis
    print("  [*] Analyzing HTTP headers...")
    try:
        response = requests.get(f"http://{TARGET_DOMAIN}", timeout=10)
        with open(f"{OUTPUT_DIR}/headers.txt", "w") as f:
            f.write("\n".join(f"{k}: {v}" for k, v in response.headers.items()))
    except Exception as e:
        print(f"    [!] HTTP headers failed: {e}")

def main():
    print(f"[*] Starting reconnaissance on {TARGET_DOMAIN}")
    print(f"[*] Results will be saved to {OUTPUT_DIR}/")
    
    # Run passive and active recon in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(passive_recon)
        executor.submit(active_recon)
    
    print("\n[+] Recon complete! Check the output directory.")

if __name__ == "__main__":
    main()