#!/usr/bin/env python3
import nmap
import argparse
import socket
from datetime import datetime

def resolve_domain_to_ip(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Could not resolve {target}")
        exit(1)

def nmap_scan(target, ports="1-1000", arguments="-sV -T4"):
    scanner = nmap.PortScanner()
    print(f"[*] Scanning {target}...")
    
    try:
        scanner.scan(target, ports=ports, arguments=arguments)
        return scanner
    except nmap.PortScannerError as e:
        print(f"[!] Nmap error: {e}")
        exit(1)

def save_results(scanner, output_file):
    with open(output_file, 'w') as f:
        for host in scanner.all_hosts():
            f.write(f"\n[+] Scan results for {host}:\n")
            f.write(f"Status: {scanner[host].state()}\n")
            for proto in scanner[host].all_protocols():
                f.write(f"\nProtocol: {proto}\n")
                ports = scanner[host][proto].keys()
                for port in ports:
                    f.write(f"Port {port}: {scanner[host][proto][port]['state']} | Service: {scanner[host][proto][port]['name']} | Version: {scanner[host][proto][port].get('version', 'N/A')}\n")

def main():
    parser = argparse.ArgumentParser(description="Fast Nmap Scanner")
    parser.add_argument("target", help="IP or domain to scan")
    parser.add_argument("-p", "--ports", default="1-1000", help="Port range (default: 1-1000)")
    parser.add_argument("-o", "--output", default="scan_results.txt", help="Output file (default: scan_results.txt)")
    args = parser.parse_args()

    # Resolve domain to IP if needed
    target = args.target if args.target.replace('.', '').isdigit() else resolve_domain_to_ip(args.target)
    
    # Run scan and save results
    scanner = nmap_scan(target, ports=args.ports)
    save_results(scanner, args.output)
    print(f"[+] Results saved to {args.output}")

if __name__ == "__main__":
    main()