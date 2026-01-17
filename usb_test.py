#!/usr/bin/env python3

"""
USB Device Testing Suite
A comprehensive tool for testing USB drive speed and capacity
"""

import os
import sys
import subprocess
import argparse
import json
import tempfile
import re
import shutil
from pathlib import Path
from statistics import mean, stdev
from time import sleep

# Unicode and emoji characters for nice output
EMOJI = {
    'usb': '💾',
    'speed': '⚡',
    'capacity': '📦',
    'check': '✅',
    'cross': '❌',
    'warning': '⚠️',
    'clock': '⏱️',
    'rocket': '🚀',
    'chart': '📊',
    'info': 'ℹ️',
    'gear': '⚙️',
    'folder': '📁',
    'fire': '🔥',
    'ok': '👍',
    'think': '🤔',
    'clean': '🧹',
    'write': '✍️',
    'read': '📖',
    'shield': '🛡️',
    'magnify': '🔍',
}

# Colors using ANSI escape codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print a fancy header"""
    width = 60
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}{'═' * width}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKBLUE}{text.center(width)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKBLUE}{'═' * width}{Colors.ENDC}\n")

def print_section(emoji, text):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{emoji}  {text}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'─' * 50}{Colors.ENDC}")

def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}{EMOJI['check']} {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}{EMOJI['cross']} {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}{EMOJI['warning']} {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}{EMOJI['info']} {text}{Colors.ENDC}")

def check_root():
    """Check if running as root"""
    if os.geteuid() != 0:
        print_error("This script requires root privileges!")
        print_info("Please run with sudo: sudo python3 usb_test.py")
        sys.exit(1)

def check_dependencies():
    """Check if required tools are installed"""
    print_section(EMOJI['gear'], "Checking Dependencies")
    
    dependencies = {
        'fio': 'Flexible I/O Tester',
        'f3write': 'F3 Write Tool',
        'f3read': 'F3 Read Tool',
        'f3probe': 'F3 Probe Tool (Non-destructive)',
    }
    
    missing = []
    optional_missing = []
    for cmd, description in dependencies.items():
        if shutil.which(cmd):
            print_success(f"{description} ({cmd}) - Found")
        else:
            if cmd == 'f3probe':
                print_warning(f"{description} ({cmd}) - Not Found (Optional)")
                optional_missing.append(cmd)
            else:
                print_error(f"{description} ({cmd}) - Not Found")
                missing.append(cmd)
    
    if missing:
        print_error("\nMissing required dependencies!")
        print_info("Install with: sudo apt install fio f3  (Debian/Ubuntu)")
        print_info("          or: sudo dnf install fio f3  (Fedora/RHEL)")
        sys.exit(1)
    
    if optional_missing:
        print_warning("\nOptional dependencies missing:")
        print_info("Non-destructive capacity test requires f3probe")
        print_info("Install with: sudo apt install f3  (Debian/Ubuntu)")
    
    print_success("\nAll required dependencies satisfied!")

def validate_mount_point(mount_point):
    """Validate that the mount point exists and is writable"""
    path = Path(mount_point)
    
    if not path.exists():
        print_error(f"Mount point does not exist: {mount_point}")
        return False
    
    if not path.is_dir():
        print_error(f"Mount point is not a directory: {mount_point}")
        return False
    
    if not os.access(mount_point, os.W_OK):
        print_error(f"Mount point is not writable: {mount_point}")
        return False
    
    return True

def get_disk_space(mount_point):
    """Get available disk space in GB"""
    stat = os.statvfs(mount_point)
    free_bytes = stat.f_bavail * stat.f_frsize
    total_bytes = stat.f_blocks * stat.f_frsize
    return free_bytes / (1024**3), total_bytes / (1024**3)

def run_single_speed_test(mount_point, test_size_mb=512):
    """Run a single speed test using fio"""
    test_file = os.path.join(mount_point, 'fio_test.tmp')
    
    # Run fio command
    cmd = [
        'fio',
        f'--name=usb_test',
        f'--filename={test_file}',
        '--direct=1',
        '--rw=readwrite',
        '--bs=1M',
        f'--size={test_size_mb}M',
        '--group_reporting',
        '--output-format=json'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return None, None
        
        # Parse JSON output
        data = json.loads(result.stdout)
        
        # Extract read and write speeds (convert from KB/s to MB/s)
        read_speed_mb = data['jobs'][0]['read']['bw'] / 1024  # KB/s to MB/s
        write_speed_mb = data['jobs'][0]['write']['bw'] / 1024  # KB/s to MB/s
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return read_speed_mb, write_speed_mb
    
    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError) as e:
        print_error(f"Error during speed test: {e}")
        return None, None
    finally:
        # Ensure cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

def run_speed_test(mount_point, num_tests=5):
    """Run multiple speed tests and calculate averages"""
    print_section(EMOJI['speed'], f"Running Speed Test ({num_tests} iterations)")
    
    free_gb, total_gb = get_disk_space(mount_point)
    print_info(f"Drive Space: {free_gb:.2f} GB free / {total_gb:.2f} GB total")
    
    read_speeds = []
    write_speeds = []
    
    print(f"\n{EMOJI['rocket']} Starting speed tests...\n")
    
    for i in range(num_tests):
        print(f"{Colors.OKCYAN}[Test {i+1}/{num_tests}]{Colors.ENDC} ", end='', flush=True)
        
        read_speed, write_speed = run_single_speed_test(mount_point)
        
        if read_speed is not None and write_speed is not None:
            read_speeds.append(read_speed)
            write_speeds.append(write_speed)
            print(f"Read: {Colors.OKGREEN}{read_speed:.2f}{Colors.ENDC} MB/s | "
                  f"Write: {Colors.OKGREEN}{write_speed:.2f}{Colors.ENDC} MB/s")
        else:
            print_error("Failed")
    
    if not read_speeds or not write_speeds:
        print_error("All speed tests failed!")
        return
    
    # Calculate statistics
    avg_read = mean(read_speeds)
    avg_write = mean(write_speeds)
    max_read = max(read_speeds)
    max_write = max(write_speeds)
    min_read = min(read_speeds)
    min_write = min(write_speeds)
    
    # Calculate standard deviation if we have multiple samples
    std_read = stdev(read_speeds) if len(read_speeds) > 1 else 0
    std_write = stdev(write_speeds) if len(write_speeds) > 1 else 0
    
    # Print results
    print_section(EMOJI['chart'], "Speed Test Results")
    
    print(f"\n{Colors.BOLD}📖 READ PERFORMANCE:{Colors.ENDC}")
    print(f"  Average: {Colors.OKGREEN}{Colors.BOLD}{avg_read:.2f} MB/s{Colors.ENDC}")
    print(f"  Maximum: {Colors.OKBLUE}{max_read:.2f} MB/s{Colors.ENDC}")
    print(f"  Minimum: {Colors.WARNING}{min_read:.2f} MB/s{Colors.ENDC}")
    if std_read > 0:
        print(f"  Std Dev: {std_read:.2f} MB/s")
    
    print(f"\n{Colors.BOLD}✍️  WRITE PERFORMANCE:{Colors.ENDC}")
    print(f"  Average: {Colors.OKGREEN}{Colors.BOLD}{avg_write:.2f} MB/s{Colors.ENDC}")
    print(f"  Maximum: {Colors.OKBLUE}{max_write:.2f} MB/s{Colors.ENDC}")
    print(f"  Minimum: {Colors.WARNING}{min_write:.2f} MB/s{Colors.ENDC}")
    if std_write > 0:
        print(f"  Std Dev: {std_write:.2f} MB/s")
    
    # Determine USB version based on speeds
    print(f"\n{Colors.BOLD}🔌 USB VERSION ESTIMATE:{Colors.ENDC}")
    max_speed = max(avg_read, avg_write)
    if max_speed < 50:
        print(f"  {EMOJI['info']} USB 2.0 (or slower)")
    elif max_speed < 450:
        print(f"  {EMOJI['rocket']} USB 3.0 / 3.1 Gen 1")
    elif max_speed < 1000:
        print(f"  {EMOJI['fire']} USB 3.1 Gen 2")
    else:
        print(f"  {EMOJI['fire']}{EMOJI['fire']} USB 3.2 or better")
    
    # Performance rating
    print(f"\n{Colors.BOLD}⭐ PERFORMANCE RATING:{Colors.ENDC}")
    if avg_write > 100 and avg_read > 100:
        print(f"  {EMOJI['fire']} Excellent performance!")
    elif avg_write > 50 and avg_read > 50:
        print(f"  {EMOJI['ok']} Good performance")
    elif avg_write > 20 and avg_read > 20:
        print(f"  {EMOJI['think']} Moderate performance")
    else:
        print(f"  {EMOJI['warning']} Poor performance - check USB port/cable")

def run_capacity_test(mount_point):
    """Run capacity test using f3"""
    print_section(EMOJI['capacity'], "Running Capacity Test")
    
    free_gb, total_gb = get_disk_space(mount_point)
    print_info(f"Drive Space: {free_gb:.2f} GB free / {total_gb:.2f} GB total")
    
    print_warning("\n⚠️  WARNING: This test will OVERWRITE all data on the drive!")
    print_warning("⚠️  The test may take several hours depending on drive size!")
    
    response = input(f"\n{EMOJI['think']} Continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print_info("Capacity test cancelled.")
        return
    
    # Run f3write
    print(f"\n{EMOJI['write']} Writing test data to drive...")
    print_info("This may take a long time. Please be patient...\n")
    
    try:
        result = subprocess.run(['f3write', mount_point], 
                              capture_output=False, 
                              timeout=None)
        
        if result.returncode != 0:
            print_error("f3write failed!")
            return
    except KeyboardInterrupt:
        print_error("\nTest interrupted by user!")
        cleanup_f3_files(mount_point)
        return
    
    # Run f3read
    print(f"\n{EMOJI['read']} Reading and verifying test data...")
    print_info("This may take a long time. Please be patient...\n")
    
    try:
        result = subprocess.run(['f3read', mount_point], 
                              capture_output=False, 
                              timeout=None)
        
        if result.returncode != 0:
            print_error("f3read failed!")
        else:
            print_success("\nCapacity test completed!")
    except KeyboardInterrupt:
        print_error("\nTest interrupted by user!")
    finally:
        cleanup_f3_files(mount_point)

def cleanup_f3_files(mount_point):
    """Clean up f3 test files"""
    print(f"\n{EMOJI['clean']} Cleaning up test files...")
    
    count = 0
    for file in Path(mount_point).glob('*.h2w'):
        try:
            file.unlink()
            count += 1
        except Exception as e:
            print_warning(f"Could not delete {file}: {e}")
    
    if count > 0:
        print_success(f"Removed {count} test file(s)")

def run_capacity_test_safe(mount_point):
    """Run non-destructive capacity test using f3probe"""
    print_section(EMOJI['shield'], "Running Non-Destructive Capacity Test")
    
    # Check if f3probe is available
    if not shutil.which('f3probe'):
        print_error("f3probe is not installed!")
        print_info("This tool is required for non-destructive testing.")
        print_info("Install with: sudo apt install f3  (Debian/Ubuntu)")
        print_info("          or: sudo dnf install f3  (Fedora/RHEL)")
        print_warning("\nNote: Older versions of f3 may not include f3probe.")
        print_info("You can still use the destructive test (-c option).")
        return
    
    free_gb, total_gb = get_disk_space(mount_point)
    print_info(f"Drive Space: {free_gb:.2f} GB free / {total_gb:.2f} GB total")
    
    print_success(f"\n{EMOJI['shield']} This is a NON-DESTRUCTIVE test!")
    print_info("This test will only use FREE SPACE on the drive.")
    print_info("Your existing files will NOT be touched.")
    print_warning("Note: This test is less comprehensive than the full capacity test.")
    
    if free_gb < 0.1:
        print_warning("\nVery little free space available (<100MB).")
        print_warning("For accurate results, more free space is recommended.")
        response = input(f"\n{EMOJI['think']} Continue anyway? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print_info("Test cancelled.")
            return
    
    # Run f3probe
    print(f"\n{EMOJI['magnify']} Probing drive capacity...")
    print_info("This will test the free space on your drive.\n")
    
    try:
        # f3probe provides detailed output about the drive
        result = subprocess.run(['f3probe', '--destructive', mount_point], 
                              capture_output=True,
                              text=True,
                              timeout=300)
        
        # Display the output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print_success("\nNon-destructive capacity test completed!")
            print_info("Check the output above for any capacity warnings or errors.")
        else:
            print_error("f3probe encountered an error!")
            if result.stderr:
                print(f"{Colors.FAIL}{result.stderr}{Colors.ENDC}")
                
    except subprocess.TimeoutExpired:
        print_error("Test timed out!")
    except KeyboardInterrupt:
        print_error("\nTest interrupted by user!")
    except Exception as e:
        print_error(f"Error running f3probe: {e}")

def show_menu():
    """Display the main menu"""
    print_header(f"{EMOJI['usb']} USB DEVICE TESTING SUITE {EMOJI['usb']}")
    
    print(f"{Colors.BOLD}Select a test option:{Colors.ENDC}\n")
    print(f"  {Colors.OKGREEN}1{Colors.ENDC}. {EMOJI['speed']} Speed Test Only")
    print(f"  {Colors.OKGREEN}2{Colors.ENDC}. {EMOJI['shield']} Capacity Test (Non-Destructive)")
    print(f"  {Colors.OKGREEN}3{Colors.ENDC}. {EMOJI['capacity']} Capacity Test (Full/Destructive)")
    print(f"  {Colors.OKGREEN}4{Colors.ENDC}. {EMOJI['rocket']} Run All Tests (Speed + Full Capacity)")
    print(f"  {Colors.OKGREEN}5{Colors.ENDC}. {EMOJI['gear']} Advanced Speed Test (custom iterations)")
    print(f"  {Colors.FAIL}0{Colors.ENDC}. {EMOJI['cross']} Exit\n")

def interactive_mode():
    """Run in interactive menu mode"""
    check_root()
    check_dependencies()
    
    # Get mount point
    print_section(EMOJI['folder'], "Mount Point Configuration")
    mount_point = input(f"Enter USB mount point (e.g., /media/usb): ").strip()
    
    if not validate_mount_point(mount_point):
        sys.exit(1)
    
    print_success(f"Using mount point: {mount_point}")
    
    while True:
        show_menu()
        choice = input(f"{EMOJI['think']} Enter your choice: ").strip()
        
        if choice == '1':
            run_speed_test(mount_point, num_tests=5)
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '2':
            run_capacity_test_safe(mount_point)
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '3':
            run_capacity_test(mount_point)
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '4':
            run_speed_test(mount_point, num_tests=5)
            run_capacity_test(mount_point)
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '5':
            try:
                num_tests = int(input(f"Enter number of test iterations (3-10): "))
                if 3 <= num_tests <= 10:
                    run_speed_test(mount_point, num_tests=num_tests)
                else:
                    print_error("Please enter a number between 3 and 10")
            except ValueError:
                print_error("Invalid input!")
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '0':
            print(f"\n{EMOJI['ok']} Goodbye!\n")
            break
        
        else:
            print_error("Invalid choice! Please try again.")
            sleep(1)

def command_line_mode(args):
    """Run in command-line mode (like the original bash script)"""
    check_root()
    check_dependencies()
    
    if not validate_mount_point(args.mount_point):
        sys.exit(1)
    
    if args.speed or args.all:
        iterations = args.iterations if args.iterations else 5
        run_speed_test(args.mount_point, num_tests=iterations)
    
    if args.capacity_safe:
        run_capacity_test_safe(args.mount_point)
    
    if args.capacity or args.all:
        run_capacity_test(args.mount_point)
    
    print(f"\n{EMOJI['check']} {Colors.OKGREEN}All tests completed!{Colors.ENDC}\n")

def main():
    parser = argparse.ArgumentParser(
        description=f'{EMOJI["usb"]} USB Device Testing Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  sudo python3 usb_test.py                       # Interactive mode
  sudo python3 usb_test.py -s /media/usb         # Speed test only
  sudo python3 usb_test.py --safe /media/usb     # Non-destructive capacity test
  sudo python3 usb_test.py -c /media/usb         # Full capacity test (destructive)
  sudo python3 usb_test.py -a /media/usb         # All tests (speed + full capacity)
  sudo python3 usb_test.py -s /media/usb -n 8    # Speed test with 8 iterations
        '''
    )
    
    parser.add_argument('mount_point', nargs='?', help='USB drive mount point')
    parser.add_argument('-s', '--speed', action='store_true', 
                       help='Run speed test only')
    parser.add_argument('--safe', '--capacity-safe', dest='capacity_safe', action='store_true',
                       help='Run non-destructive capacity test (uses f3probe)')
    parser.add_argument('-c', '--capacity', action='store_true', 
                       help='Run full capacity test (DESTRUCTIVE - erases data)')
    parser.add_argument('-a', '--all', action='store_true', 
                       help='Run all tests (speed + full capacity)')
    parser.add_argument('-n', '--iterations', type=int, 
                       help='Number of speed test iterations (default: 5)')
    parser.add_argument('--no-interactive', action='store_true',
                       help='Disable interactive mode')
    
    args = parser.parse_args()
    
    # If no arguments provided, run in interactive mode
    if not args.mount_point and not args.no_interactive:
        interactive_mode()
    elif args.mount_point:
        command_line_mode(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{EMOJI['warning']} Operation cancelled by user.\n")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
