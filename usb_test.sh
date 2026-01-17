#!/bin/bash

# Function to show help
show_help() {
    echo "Usage: sudo $0 [OPTION] [MOUNT_POINT]"
    echo "  -s    Speed Test Only"
    echo "  -p    Capacity Test (Non-Destructive with f3probe)"
    echo "  -c    Capacity Test (Full/Destructive)"
    echo "  -a    All Tests"
    exit 1
}

# Ensure tools are present
for cmd in fio f3write awk; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is not installed. Please run: sudo apt install fio f3"
        exit 1
    fi
done

# Check for f3probe (optional, for non-destructive test)
F3PROBE_AVAILABLE=0
if command -v f3probe &> /dev/null; then
    F3PROBE_AVAILABLE=1
fi

run_speed_test() {
    local MNT=$1
    local TEST_FILE="$MNT/fio_test.tmp"
    echo -e "\n>>> RUNNING SPEED TEST <<<"

    # Run fio and output to a temporary log
    fio --name=usb_test --filename="$TEST_FILE" --direct=1 --rw=readwrite --bs=1M --size=512M --group_reporting > /tmp/fio_results.txt

    # Extract Read and Write speeds using awk
    READ_SPD=$(awk '/READ:/ {print $2}' /tmp/fio_results.txt | sed 's/bw=//;s/MiB\/s//;s/(//;s/)//')
    WRITE_SPD=$(awk '/WRITE:/ {print $2}' /tmp/fio_results.txt | sed 's/bw=//;s/MiB\/s//;s/(//;s/)//')

    echo "---------------------------------------"
    echo "  Read Speed  : $READ_SPD MiB/s"
    echo "  Write Speed : $WRITE_SPD MiB/s"
    echo "---------------------------------------"

    rm -f "$TEST_FILE" /tmp/fio_results.txt
}

run_capacity_test() {
    local MNT=$1
    echo -e "\n>>> RUNNING CAPACITY TEST (f3) <<<"
    f3write "$MNT"
    f3read "$MNT"
    rm -f "$MNT"/*.h2w
}

run_capacity_test_safe() {
    local MNT=$1
    echo -e "\n>>> RUNNING NON-DESTRUCTIVE CAPACITY TEST (f3probe) <<<"
    
    if [ $F3PROBE_AVAILABLE -eq 0 ]; then
        echo "Error: f3probe is not installed."
        echo "Install with: sudo apt install f3  (Debian/Ubuntu)"
        echo "          or: sudo dnf install f3  (Fedora/RHEL)"
        echo "Note: You can still use the full capacity test with -c"
        return 1
    fi
    
    echo "This is a NON-DESTRUCTIVE test - existing files will NOT be touched."
    echo "Only free space will be tested."
    echo ""
    
    f3probe --destructive "$MNT"
    
    if [ $? -eq 0 ]; then
        echo -e "\nNon-destructive capacity test completed!"
    else
        echo -e "\nCapacity test encountered an error!"
    fi
}

# Main Logic
while getopts "spcah" opt; do
    case $opt in
        s) MODE="SPEED" ;;
        p) MODE="CAPACITY_SAFE" ;;
        c) MODE="CAPACITY" ;;
        a) MODE="ALL" ;;
        *) show_help ;;
    esac
done
shift $((OPTIND-1))

MOUNT_PATH=$1
if [[ -z "$MOUNT_PATH" ]]; then show_help; fi

if [[ "$MODE" == "SPEED" || "$MODE" == "ALL" ]]; then run_speed_test "$MOUNT_PATH"; fi
if [[ "$MODE" == "CAPACITY_SAFE" ]]; then run_capacity_test_safe "$MOUNT_PATH"; fi
if [[ "$MODE" == "CAPACITY" || "$MODE" == "ALL" ]]; then run_capacity_test "$MOUNT_PATH"; fi

echo -e "\n[Finished]"
