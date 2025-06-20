import nmap
import argparse

def run_nmap_scan(target, scan_type, ports=None, timing=None, output_file=None):
    nm = nmap.PortScanner()
    arguments = ""

    # Scan type configuration
    if scan_type == 1:    # TCP SYN Scan (Stealth)
        arguments += "-sS "
    elif scan_type == 2:  # TCP Connect Scan
        arguments += "-sT "
    elif scan_type == 3:  # UDP Scan
        arguments += "-sU "
    elif scan_type == 4:  # Ping Scan
        arguments += "-sn "
    elif scan_type == 5:  # Aggressive Scan
        arguments += "-A "
    elif scan_type == 6:  # Version Detection
        arguments += "-sV "
    elif scan_type == 7:  # OS Detection
        arguments += "-O "
    elif scan_type == 8:  # NSE Script Scan
        arguments += "-sC "
    elif scan_type == 9:  # Full Port Scan
        arguments += "-p- "
    
    # Port specification
    if ports and scan_type not in [4, 9]:  # Skip if ping scan or full port scan
        arguments += f"-p {ports} "
    
    # Timing template
    if timing and 0 <= timing <= 5:
        arguments += f"-T{timing} "
    
    # Output files
    output_cmd = ""
    if output_file:
        output_cmd = f"-oN {output_file}"

    # Combine arguments
    full_cmd = f"{arguments} {output_cmd}".strip()
    
    print(f"\n[+] Executing: nmap {full_cmd} {target}")
    
    try:
        nm.scan(target, arguments=full_cmd)
        print("\n[+] Scan Results:")
        print(nm.csv())
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(nm.csv())
            print(f"\n[+] Results saved to {output_file}")
            
    except nmap.PortScannerError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Python Nmap Scanner")
    parser.add_argument("target", help="Target IP/host or network range")
    parser.add_argument("-p", "--ports", help="Port(s) to scan (e.g., 80, 1-100)")
    parser.add_argument("-o", "--output", help="Output file name")
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print("Nmap Scanner Menu")
    print("="*50)
    print("1. TCP SYN Scan (Stealth)")
    print("2. TCP Connect Scan")
    print("3. UDP Scan")
    print("4. Host Discovery (Ping Scan)")
    print("5. Aggressive Scan (OS/Version/Script)")
    print("6. Service Version Detection")
    print("7. OS Detection")
    print("8. NSE Script Scan")
    print("9. Full Port Scan (1-65535)")
    print("0. Exit")
    
    try:
        choice = int(input("\nSelect scan type (0-9): "))
        if choice == 0:
            return
        
        if choice not in range(1, 10):
            print("Invalid selection")
            return

        timing = input("Timing (0-5, Enter for default): ")
        timing = int(timing) if timing.strip() else None

        run_nmap_scan(
            target=args.target,
            scan_type=choice,
            ports=args.ports,
            timing=timing,
            output_file=args.output
        )
        
    except ValueError:
        print("Invalid input")

if __name__ == "__main__":
    main()