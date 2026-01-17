#!/bin/bash

# Function to show help
show_help() {
    echo "Usage: sudo $0 [OPTION] [MOUNT_POINT]"
    echo "  -s    Speed Test Only"
    echo "  -c    Capacity Test (fills free space, preserves existing files)"
    echo "  -a    All Tests (Speed + Capacity)"
    echo ""
    echo "Note: Capacity test fills ALL free space but does NOT delete existing files."
    exit 1
}

# Ensure tools are present
for cmd in fio f3write f3read awk; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is not installed. Please run: sudo apt install fio f3"
        exit 1
    fi
done

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
    echo "This test fills all FREE SPACE but does NOT delete existing files."
    echo ""
    f3write "$MNT"
    f3read "$MNT"
    rm -f "$MNT"/*.h2w
    echo -e "\nYour existing files were preserved."
}

# Main Logic
while getopts "scah" opt; do
    case $opt in
        s) MODE="SPEED" ;;
        c) MODE="CAPACITY" ;;
        a) MODE="ALL" ;;
        *) show_help ;;
    esac
done
shift $((OPTIND-1))

MOUNT_PATH=$1
if [[ -z "$MOUNT_PATH" ]]; then show_help; fi

if [[ "$MODE" == "SPEED" || "$MODE" == "ALL" ]]; then run_speed_test "$MOUNT_PATH"; fi
if [[ "$MODE" == "CAPACITY" || "$MODE" == "ALL" ]]; then run_capacity_test "$MOUNT_PATH"; fi

echo -e "\n[Finished]"
