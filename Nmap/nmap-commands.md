
# Nmap Command Cheat Sheet

A comprehensive collection of Nmap commands for penetration testing, network discovery, and security auditing.

```bash
# Update Nmap and scripts
sudo nmap --script-updatedb
```

## Basic Scans

```bash
# Basic TCP scan
nmap target.com

# Scan specific port
nmap -p 80 target.com

# Scan multiple ports
nmap -p 80,443,22 target.com

# Scan port range
nmap -p 1-1000 target.com

# Scan all ports (1-65535)
nmap -p- target.com

# Fast scan (100 most common ports)
nmap -F target.com

# Scan from a file
nmap -iL targets.txt
```

## Network Discovery

```bash
# Ping scan only (discovery)
nmap -sn 192.168.1.0/24

# ARP scan (local network)
nmap -PR 192.168.1.0/24

# List scan (just list targets)
nmap -sL 192.168.1.0/24

# Exclude hosts from scan
nmap 192.168.1.0/24 --exclude 192.168.1.5
```

## Port Scanning Techniques

```bash
# SYN scan (stealth/half-open)
nmap -sS target.com

# TCP connect scan (full connection)
nmap -sT target.com

# UDP scan
nmap -sU -p 53,67,68,69,123 target.com

# ACK scan (firewall testing)
nmap -sA target.com

# Window scan (obsolete systems)
nmap -sW target.com

# Maimon scan (UNIX systems)
nmap -sM target.com
```

## Service Detection

```bash
# Service version detection
nmap -sV target.com

# Aggressive scan (-A = OS/version/script/traceroute)
nmap -A target.com

# Light version detection
nmap -sV --version-light target.com

# All out version detection
nmap -sV --version-all target.com

# RPC scan
nmap -sR target.com
```

## OS Detection

```bash
# OS detection
nmap -O target.com

# Aggressive OS detection
nmap -O --osscan-guess target.com

# Maximum OS detection attempts
nmap -O --max-os-tries 5 target.com
```

## NSE Scripting Engine

```bash
# Default safe scripts
nmap -sC target.com

# Run specific script
nmap --script=http-title target.com

# Run multiple scripts
nmap --script=http-title,http-headers target.com

# Run script categories
nmap --script=vuln target.com
nmap --script=exploit target.com
nmap --script=auth target.com
nmap --script=brute target.com

# Update script database
nmap --script-updatedb

# Debug scripts
nmap --script-trace target.com

# Set script arguments
nmap --script=http-enum --script-args http-enum.basepath=/web/ target.com
```

## Output Formats

```bash
# Normal output
nmap -oN scan.txt target.com

# XML output
nmap -oX scan.xml target.com

# Grepable output
nmap -oG scan.gnmap target.com

# All formats
nmap -oA scan target.com

# Append output
nmap -oN - append-output target.com

# Verbose output
nmap -v target.com

# Extra verbose
nmap -vv target.com
```

## Performance Options

```bash
# Timing template (0-5)
nmap -T0 target.com  # Paranoid
nmap -T1 target.com  # Sneaky
nmap -T2 target.com  # Polite
nmap -T3 target.com  # Normal
nmap -T4 target.com  # Aggressive
nmap -T5 target.com  # Insane

# Host timeout
nmap --host-timeout 30m target.com

# Min parallel hosts
nmap --min-parallelism 100 target.com

# Max retries
nmap --max-retries 3 target.com

# Min rate (packets/sec)
nmap --min-rate 500 target.com

# Max rate
nmap --max-rate 1500 target.com
```

## Firewall Evasion

```bash
# Fragment packets
nmap -f target.com

# More fragments
nmap -ff target.com

# Custom MTU
nmap --mtu 24 target.com

# Decoy scan
nmap -D RND:10 target.com  # Random 10 IPs
nmap -D decoy1,decoy2,ME target.com

# Source port specification
nmap --source-port 53 target.com

# Spoof MAC address
nmap --spoof-mac Cisco target.com

# Bad checksum
nmap --badsum target.com

# Idle/zombie scan
nmap -sI zombie.com:80 target.com
```

## Advanced Techniques

```bash
# IP protocol scan
nmap -sO target.com

# Traceroute
nmap --traceroute target.com

# Append random data
nmap --data-length 25 target.com

# Send hex data
nmap --data-string "\x01\x02\x03" target.com

# Scan IPv6 targets
nmap -6 target.com

# Scan through HTTP proxy
nmap --proxies http://proxy:8080 target.com
```

## Vulnerability Scanning

```bash
# Run all vuln scripts
nmap --script vuln target.com

# Run exploit scripts
nmap --script exploit target.com

# Safe scripts only
nmap --script safe target.com

# Malware detection
nmap --script malware target.com

# Brute force attacks
nmap --script brute target.com

# HTTP enumeration
nmap --script http-enum target.com

# SSL scanning
nmap --script ssl-enum-ciphers -p 443 target.com
```

## Useful Combinations

```bash
# Comprehensive scan
nmap -sS -sU -T4 -A -v -p- target.com

# Quick scan with service detection
nmap -T4 -F -sV target.com

# Stealthy scan
nmap -sS -sV -T2 --max-parallelism 1 --max-retries 3 -f target.com

# Full port UDP scan
nmap -sU -T4 -p- -v --max-retries 1 target.com
```

## Troubleshooting

```bash
# Debug output
nmap -d target.com

# Packet trace
nmap --packet-trace target.com

# Interface selection
nmap -e eth0 target.com

# DNS resolution control
nmap -n target.com  # Never resolve
nmap -R target.com  # Always resolve
```