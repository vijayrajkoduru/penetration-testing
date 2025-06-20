#!/bin/bash

# Prompt user for target input
read -p "Enter target IP/hostname/domain/subnet or filename with -iL: " TARGET

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR="nmap_scans_${TIMESTAMP}"
mkdir -p $OUTPUT_DIR

echo -e "\nStarting comprehensive Nmap scans against $TARGET..."
echo "Results will be saved to $OUTPUT_DIR/"

# Function to run scans with error handling
run_scan() {
    local scan_name=$1
    local scan_cmd=$2
    local output_file=$3
    
    echo -e "\nRunning $scan_name..."
    echo "Command: $scan_cmd"
    
    eval $scan_cmd 2>&1 | tee $output_file
    
    # Check if scan failed
    if [ ${PIPESTATUS[0]} -ne 0 ]; then
        echo "Warning: $scan_name scan failed or was interrupted" | tee -a $output_file
    fi
}

# Basic Scans
run_scan "Basic Scan" "nmap -v $TARGET" "$OUTPUT_DIR/1_basic_scan.txt"

# Only run file scan if target ends with .txt
if [[ $TARGET == *.txt ]]; then
    run_scan "File Input Scan" "nmap -v -iL $TARGET" "$OUTPUT_DIR/2_file_scan.txt"
fi

# Port-specific Scans
run_scan "Single Port (80)" "nmap -v -p 80 $TARGET" "$OUTPUT_DIR/3_single_port_80.txt"
run_scan "Multiple Ports (80,443,22)" "nmap -v -p 80,443,22 $TARGET" "$OUTPUT_DIR/4_multi_ports.txt"
run_scan "Port Range (1-1000)" "nmap -v -p 1-1000 $TARGET" "$OUTPUT_DIR/5_port_range_1-1000.txt"
run_scan "All Ports" "nmap -v -p- $TARGET" "$OUTPUT_DIR/6_all_ports.txt"
run_scan "Fast Scan (Top 100)" "nmap -v -F $TARGET" "$OUTPUT_DIR/7_fast_scan_top100.txt"
run_scan "Top 50 Ports" "nmap -v --top-ports 50 $TARGET" "$OUTPUT_DIR/8_top_50_ports.txt"

# Scan Techniques
run_scan "Stealth SYN Scan" "nmap -v -sS $TARGET" "$OUTPUT_DIR/9_stealth_syn.txt"
run_scan "TCP Connect Scan" "nmap -v -sT $TARGET" "$OUTPUT_DIR/10_tcp_connect.txt"
run_scan "UDP Scan" "nmap -v -sU $TARGET" "$OUTPUT_DIR/11_udp_scan.txt"
run_scan "NULL Scan" "nmap -v -sN $TARGET" "$OUTPUT_DIR/12_null_scan.txt"
run_scan "FIN Scan" "nmap -v -sF $TARGET" "$OUTPUT_DIR/13_fin_scan.txt"
run_scan "XMAS Scan" "nmap -v -sX $TARGET" "$OUTPUT_DIR/14_xmas_scan.txt"
run_scan "ACK Scan" "nmap -v -sA $TARGET" "$OUTPUT_DIR/15_ack_scan.txt"

# Service and OS Detection
run_scan "Service Version Detection" "nmap -v -sV $TARGET" "$OUTPUT_DIR/16_service_versions.txt"
run_scan "OS Fingerprinting" "nmap -v -O $TARGET" "$OUTPUT_DIR/17_os_fingerprint.txt"
run_scan "Aggressive Scan" "nmap -v -A $TARGET" "$OUTPUT_DIR/18_aggressive_scan.txt"
run_scan "Deep Version Detection" "nmap -v --version-intensity 9 $TARGET" "$OUTPUT_DIR/19_deep_version.txt"

# Vulnerability Scanning
run_scan "Vulnerability Scripts" "nmap -v --script vuln $TARGET" "$OUTPUT_DIR/20_vuln_scan.txt"
run_scan "HTTP Scripts" "nmap -v --script=http* $TARGET" "$OUTPUT_DIR/21_http_scripts.txt"
run_scan "SMB Vulnerability Checks" "nmap -v --script=smb-vuln* -p 445 $TARGET" "$OUTPUT_DIR/22_smb_vulns.txt"

# Specialized Scans
run_scan "SSH Brute Force Check" "nmap -v -sS -p 22 --script ssh-brute $TARGET" "$OUTPUT_DIR/23_ssh_brute.txt"
run_scan "WHOIS Lookup" "nmap -v --script whois-domain $TARGET" "$OUTPUT_DIR/24_whois.txt"
run_scan "Ping Sweep" "nmap -v -sn $TARGET" "$OUTPUT_DIR/25_ping_sweep.txt"
run_scan "Traceroute" "nmap -v --traceroute $TARGET" "$OUTPUT_DIR/26_traceroute.txt"

# Comprehensive Scans
run_scan "Full Stealth Scan" "nmap -v -sS -O -T4 -p- -A $TARGET" "$OUTPUT_DIR/27_full_stealth_scan.txt"
run_scan "Web Server Detection" "nmap -v -p 80,443,8080 -sV --open $TARGET" "$OUTPUT_DIR/28_web_servers.txt"
run_scan "SMB Host Detection" "nmap -v -p 445 --open $TARGET" "$OUTPUT_DIR/29_smb_hosts.txt"

# Generate all output formats for the comprehensive scan
run_scan "Comprehensive Scan (All Formats)" "nmap -v -A -T4 $TARGET -oA $OUTPUT_DIR/30_comprehensive" "/dev/null"

# Quick open ports summary
echo -e "\n=== QUICK OPEN PORTS SUMMARY ==="
nmap -v -p 80,443 $TARGET | grep "open" | tee $OUTPUT_DIR/31_open_ports_summary.txt

echo -e "\n=== SCAN COMPLETED ==="
echo "All results saved to $OUTPUT_DIR/"
echo -e "\nQuick summary of open ports (80,443):"
cat $OUTPUT_DIR/31_open_ports_summary.txt

echo -e "\nTo view any scan results:"
echo "cat $OUTPUT_DIR/<scan_file>.txt"