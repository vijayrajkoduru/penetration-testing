#!/bin/bash

# Nmap Scanner Script
# A simple interactive wrapper for common Nmap scans

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color


# Function to display menu
show_menu() {
    echo -e "\n${YELLOW}Select a scan type:${NC}"
    echo "1. Basic TCP scan (nmap target.com)"
    echo "2. Scan specific port (nmap -p 80 target.com)"
    echo "3. Scan multiple ports (nmap -p 80,443,22 target.com)"
    echo "4. Scan port range (nmap -p 1-1000 target.com)"
    echo "5. Scan all ports (nmap -p- target.com)"
    echo "6. Fast scan (nmap -F target.com)"
    echo "7. Scan from file (nmap -iL targets.txt)"
    echo "8. Exit"
    echo -n "Enter your choice [1-8]: "
}

# Function to get target
get_target() {
    echo -n "Enter target (IP/hostname): "
    read target
    if [ -z "$target" ]; then
        echo -e "${RED}Error: Target cannot be empty${NC}"
        return 1
    fi
    return 0
}

# Function to confirm and run command
run_scan() {
    echo -e "\n${GREEN}Command to execute:${NC} $1"
    echo -n "Proceed? [y/N]: "
    read confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Scanning...${NC}\n"
        eval $1
    else
        echo -e "${YELLOW}Scan canceled${NC}"
    fi
}

# Main loop
while true; do
    show_menu
    read choice
    
    case $choice in
        1)
            if get_target; then
                cmd="nmap $target"
                run_scan "$cmd"
            fi
            ;;
        2)
            if get_target; then
                echo -n "Enter port number: "
                read port
                if [[ "$port" =~ ^[0-9]+$ ]]; then
                    cmd="nmap -p $port $target"
                    run_scan "$cmd"
                else
                    echo -e "${RED}Error: Invalid port number${NC}"
                fi
            fi
            ;;
        3)
            if get_target; then
                echo -n "Enter ports (comma separated): "
                read ports
                if [[ "$ports" =~ ^[0-9,]+$ ]]; then
                    cmd="nmap -p $ports $target"
                    run_scan "$cmd"
                else
                    echo -e "${RED}Error: Invalid port list${NC}"
                fi
            fi
            ;;
        4)
            if get_target; then
                echo -n "Enter port range (start-end): "
                read port_range
                if [[ "$port_range" =~ ^[0-9]+-[0-9]+$ ]]; then
                    cmd="nmap -p $port_range $target"
                    run_scan "$cmd"
                else
                    echo -e "${RED}Error: Invalid port range${NC}"
                fi
            fi
            ;;
        5)
            if get_target; then
                cmd="nmap -p- $target"
                run_scan "$cmd"
            fi
            ;;
        6)
            if get_target; then
                cmd="nmap -F $target"
                run_scan "$cmd"
            fi
            ;;
        7)
            echo -n "Enter path to targets file: "
            read target_file
            if [ -f "$target_file" ]; then
                cmd="nmap -iL $target_file"
                run_scan "$cmd"
            else
                echo -e "${RED}Error: File not found${NC}"
            fi
            ;;
        8)
            echo -e "${GREEN}Exiting...${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option, please try again${NC}"
            ;;
    esac
done