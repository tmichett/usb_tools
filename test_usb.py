#!/usr/bin/env python3

"""
Cross-Platform USB Device Testing Suite
Works on Windows, macOS, and Linux without external dependencies
"""

import os
import sys
import time
import platform
import argparse
import hashlib
import shutil
from pathlib import Path
from statistics import mean, stdev
from datetime import datetime

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
    'computer': '💻',
    'windows': '🪟',
    'apple': '🍎',
    'linux': '🐧',
}

# Colors using ANSI escape codes (works on modern terminals)
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

# Enable ANSI colors on Windows
if platform.system() == 'Windows':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass

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

def get_platform_info():
    """Get current platform information"""
    system = platform.system()
    if system == 'Windows':
        return 'Windows', EMOJI['windows']
    elif system == 'Darwin':
        return 'macOS', EMOJI['apple']
    elif system == 'Linux':
        return 'Linux', EMOJI['linux']
    else:
        return system, EMOJI['computer']

def validate_path(path):
    """Validate that the path exists and is writable"""
    path_obj = Path(path)
    
    if not path_obj.exists():
        print_error(f"Path does not exist: {path}")
        return False
    
    if not path_obj.is_dir():
        print_error(f"Path is not a directory: {path}")
        return False
    
    # Test write permissions
    test_file = path_obj / '.test_write_permission'
    try:
        test_file.touch()
        test_file.unlink()
    except (PermissionError, OSError) as e:
        print_error(f"Path is not writable: {path}")
        print_error(f"Error: {e}")
        return False
    
    return True

def get_disk_space(path):
    """Get available disk space in GB"""
    stat = shutil.disk_usage(path)
    free_gb = stat.free / (1024**3)
    total_gb = stat.total / (1024**3)
    used_gb = stat.used / (1024**3)
    return free_gb, total_gb, used_gb

def format_bytes(bytes_val):
    """Format bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"

def generate_test_data(size_mb):
    """Generate test data with a known pattern"""
    # Create a repeating pattern that's easy to verify
    pattern = b'USB_TEST_' + os.urandom(54)  # 64 bytes total
    chunk_size = 1024 * 1024  # 1 MB
    
    # Pre-generate 1MB of pattern
    mb_pattern = pattern * (chunk_size // len(pattern))
    
    # Return generator for memory efficiency
    for _ in range(size_mb):
        yield mb_pattern

def run_write_test(path, size_mb, label="Write"):
    """Run a write speed test"""
    test_file = Path(path) / f'speed_test_{int(time.time())}.tmp'
    
    try:
        start_time = time.time()
        bytes_written = 0
        
        # Use unbuffered writes
        with open(test_file, 'wb', buffering=0) as f:
            for chunk in generate_test_data(size_mb):
                f.write(chunk)
                bytes_written += len(chunk)
                # Periodic fsync to ensure writes go to disk
                if bytes_written % (10 * 1024 * 1024) == 0:  # Every 10MB
                    os.fsync(f.fileno())
            
            # Final sync
            os.fsync(f.fileno())
        
        end_time = time.time()
        duration = end_time - start_time
        
        if duration > 0:
            speed_mb = size_mb / duration
            return speed_mb, test_file
        else:
            return None, test_file
    
    except Exception as e:
        print_error(f"{label} test failed: {e}")
        if test_file.exists():
            test_file.unlink()
        return None, None

def clear_cache():
    """Attempt to clear OS cache (platform-specific)"""
    system = platform.system()
    
    if system == 'Linux':
        # Try to drop caches on Linux (requires root)
        try:
            # Clear PageCache, dentries and inodes
            with open('/proc/sys/vm/drop_caches', 'w') as f:
                f.write('3\n')
        except (PermissionError, FileNotFoundError):
            # If we can't drop caches, at least sync
            try:
                os.sync()
            except:
                pass
    else:
        # On Windows/macOS, just sync what we can
        try:
            os.sync()
        except:
            pass

def run_read_test(test_file, size_mb, label="Read"):
    """Run a read speed test with cache avoidance"""
    try:
        # Try to clear cache before reading
        clear_cache()
        
        # Small delay to let cache clearing take effect
        time.sleep(0.5)
        
        start_time = time.time()
        bytes_read = 0
        chunk_size = 1024 * 1024  # 1 MB
        
        # Open with minimal buffering
        with open(test_file, 'rb', buffering=0) as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                bytes_read += len(chunk)
                # Force CPU to process the data (prevent optimization)
                _ = len(chunk)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if duration > 0:
            speed_mb = size_mb / duration
            return speed_mb
        else:
            return None
    
    except Exception as e:
        print_error(f"{label} test failed: {e}")
        return None

def run_speed_test_iteration(path, test_size_mb=512):
    """Run a single iteration of speed test"""
    # Write test
    write_speed, test_file = run_write_test(path, test_size_mb)
    
    if write_speed is None or test_file is None:
        return None, None
    
    # Read test
    read_speed = run_read_test(test_file, test_size_mb)
    
    # Cleanup
    try:
        if test_file and test_file.exists():
            test_file.unlink()
    except:
        pass
    
    return read_speed, write_speed

def run_speed_tests(path, num_tests=5, test_size_mb=512):
    """Run multiple speed tests and calculate statistics"""
    print_section(EMOJI['speed'], f"Running Speed Tests ({num_tests} iterations)")
    
    free_gb, total_gb, used_gb = get_disk_space(path)
    print_info(f"Drive Space: {used_gb:.2f} GB used / {free_gb:.2f} GB free / {total_gb:.2f} GB total")
    
    # Warning about cache on Linux
    if platform.system() == 'Linux':
        try:
            if os.geteuid() != 0:
                print_warning("Note: Running without sudo - read speeds may show cache effects")
                print_info("For accurate results, run with: sudo python3 test_usb.py")
        except AttributeError:
            pass  # geteuid() not available on this platform
    
    # Check if we have enough space
    required_gb = (test_size_mb / 1024) * 1.5  # 50% buffer
    if free_gb < required_gb:
        print_warning(f"Insufficient space for testing. Need {required_gb:.1f} GB, have {free_gb:.1f} GB")
        print_info("Reducing test size...")
        test_size_mb = int((free_gb - 0.5) * 1024)
        if test_size_mb < 50:
            print_error("Not enough space for meaningful speed test (need at least 0.5 GB free)")
            return
    
    print_info(f"Test size: {test_size_mb} MB per iteration")
    print_info(f"Total data: {(test_size_mb * num_tests) / 1024:.1f} GB")
    
    # Provide guidance on test size
    if test_size_mb < 512:
        print_warning("Small test size - may not be accurate for fast drives")
    elif test_size_mb >= 2048:
        print_success("Large test size - excellent for high-performance drives")
    
    print(f"\n{EMOJI['rocket']} Starting speed tests...\n")
    
    read_speeds = []
    write_speeds = []
    
    for i in range(num_tests):
        print(f"{Colors.OKCYAN}[Test {i+1}/{num_tests}]{Colors.ENDC} ", end='', flush=True)
        
        read_speed, write_speed = run_speed_test_iteration(path, test_size_mb)
        
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
    
    # USB version estimate
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
        print(f"  {EMOJI['warning']} Poor performance")

def run_capacity_test(path, test_size_gb=5):
    """Run capacity test by writing and verifying data"""
    print_section(EMOJI['capacity'], f"Running Capacity Test ({test_size_gb} GB)")
    
    free_gb, total_gb, used_gb = get_disk_space(path)
    print_info(f"Drive Space: {used_gb:.2f} GB used / {free_gb:.2f} GB free / {total_gb:.2f} GB total")
    
    # Adjust test size if necessary
    max_test_gb = free_gb - 0.5  # Leave 500MB buffer
    if test_size_gb > max_test_gb:
        test_size_gb = max(1, int(max_test_gb))
        print_warning(f"Adjusted test size to {test_size_gb} GB based on available space")
    
    if test_size_gb < 1:
        print_error("Insufficient free space for capacity test (need at least 1.5 GB)")
        return
    
    # Warn if testing large capacity
    if test_size_gb >= free_gb - 1:
        print_success(f"\n{EMOJI['capacity']} Full Capacity Test - Testing {test_size_gb} GB (ALL free space)")
        print_warning("This will temporarily FILL the entire drive!")
    elif test_size_gb >= 20:
        print_success(f"\n{EMOJI['capacity']} Large Capacity Test - Testing {test_size_gb} GB")
        print_info("This is a thorough test for high-capacity drives")
    else:
        print_success(f"\n{EMOJI['shield']} Quick Capacity Test - Testing {test_size_gb} GB")
    
    print_info("This test writes data with checksums and verifies it")
    print_info("Your existing files will NOT be touched")
    
    estimated_time = int(test_size_gb * 2)  # Rough estimate
    print_info(f"\n{EMOJI['clock']} Estimated time: ~{estimated_time} minutes")
    
    response = input(f"\n{EMOJI['think']} Continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print_info("Capacity test cancelled")
        return
    
    # Create test files
    test_dir = Path(path) / f'capacity_test_{int(time.time())}'
    test_dir.mkdir(exist_ok=True)
    
    file_size_mb = 100  # 100MB per file
    num_files = test_size_gb * 10  # 10 files per GB
    
    print(f"\n{EMOJI['write']} Phase 1: Writing test data...")
    
    checksums = {}
    bytes_written = 0
    start_time = time.time()
    
    try:
        for i in range(num_files):
            file_path = test_dir / f'test_{i:04d}.dat'
            
            # Progress indicator
            progress = (i + 1) / num_files * 100
            print(f"  Writing file {i+1}/{num_files} ({progress:.1f}%)... ", end='', flush=True)
            
            # Generate data with hash
            hasher = hashlib.sha256()
            
            with open(file_path, 'wb') as f:
                for chunk in generate_test_data(file_size_mb):
                    f.write(chunk)
                    hasher.update(chunk)
                    bytes_written += len(chunk)
            
            checksums[file_path.name] = hasher.hexdigest()
            print(f"{Colors.OKGREEN}OK{Colors.ENDC}")
        
        write_time = time.time() - start_time
        write_speed = (bytes_written / (1024**2)) / write_time if write_time > 0 else 0
        
        print_success(f"\nWrote {format_bytes(bytes_written)} in {write_time:.1f}s ({write_speed:.2f} MB/s)")
        
        # Verification phase
        print(f"\n{EMOJI['read']} Phase 2: Verifying data integrity...")
        
        errors = 0
        bytes_verified = 0
        start_time = time.time()
        
        for i, (filename, expected_hash) in enumerate(checksums.items()):
            file_path = test_dir / filename
            
            progress = (i + 1) / len(checksums) * 100
            print(f"  Verifying file {i+1}/{len(checksums)} ({progress:.1f}%)... ", end='', flush=True)
            
            if not file_path.exists():
                print(f"{Colors.FAIL}MISSING{Colors.ENDC}")
                errors += 1
                continue
            
            # Verify size
            actual_size = file_path.stat().st_size
            expected_size = file_size_mb * 1024 * 1024
            
            if actual_size != expected_size:
                print(f"{Colors.FAIL}SIZE MISMATCH{Colors.ENDC}")
                errors += 1
                continue
            
            # Verify checksum
            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                while chunk := f.read(1024 * 1024):
                    hasher.update(chunk)
                    bytes_verified += len(chunk)
            
            actual_hash = hasher.hexdigest()
            
            if actual_hash == expected_hash:
                print(f"{Colors.OKGREEN}OK{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}CORRUPTED{Colors.ENDC}")
                errors += 1
        
        read_time = time.time() - start_time
        read_speed = (bytes_verified / (1024**2)) / read_time if read_time > 0 else 0
        
        print_success(f"\nVerified {format_bytes(bytes_verified)} in {read_time:.1f}s ({read_speed:.2f} MB/s)")
        
        # Results
        print_section(EMOJI['chart'], "Capacity Test Results")
        
        if errors == 0:
            print_success(f"\n{EMOJI['check']} ALL TESTS PASSED!")
            print_info(f"Tested {test_size_gb} GB successfully")
            print_info("No data corruption detected")
            print_info("Drive capacity appears genuine")
        else:
            print_error(f"\n{EMOJI['cross']} {errors} ERROR(S) DETECTED!")
            print_warning("Drive may have capacity issues or be counterfeit")
            print_warning("Some data was corrupted or lost")
    
    except KeyboardInterrupt:
        print_error("\n\nTest interrupted by user!")
    except Exception as e:
        print_error(f"\nTest error: {e}")
    finally:
        # Cleanup
        print(f"\n{EMOJI['clean']} Cleaning up test files...")
        try:
            shutil.rmtree(test_dir)
            print_success("Cleanup complete")
        except Exception as e:
            print_warning(f"Could not remove test directory: {e}")
            print_info(f"Manually delete: {test_dir}")

def show_menu():
    """Display main menu"""
    print_header(f"{EMOJI['usb']} USB DEVICE TESTING SUITE {EMOJI['usb']}")
    
    os_name, os_emoji = get_platform_info()
    print(f"{Colors.BOLD}Platform: {os_emoji} {os_name}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Select a test option:{Colors.ENDC}\n")
    print(f"  {Colors.OKGREEN}1{Colors.ENDC}. {EMOJI['speed']} Speed Test - Standard (5x 512MB)")
    print(f"  {Colors.OKGREEN}2{Colors.ENDC}. {EMOJI['fire']} Speed Test - High Performance (5x 2GB)")
    print(f"  {Colors.OKGREEN}3{Colors.ENDC}. {EMOJI['shield']} Capacity Test - Quick (5 GB)")
    print(f"  {Colors.OKGREEN}4{Colors.ENDC}. {EMOJI['capacity']} Capacity Test - Full (All Free Space)")
    print(f"  {Colors.OKGREEN}5{Colors.ENDC}. {EMOJI['rocket']} Run All Tests (Standard + Full Capacity)")
    print(f"  {Colors.OKGREEN}6{Colors.ENDC}. {EMOJI['gear']} Custom Speed Test")
    print(f"  {Colors.OKGREEN}7{Colors.ENDC}. {EMOJI['gear']} Custom Capacity Test")
    print(f"  {Colors.FAIL}0{Colors.ENDC}. {EMOJI['cross']} Exit\n")
    print(f"{Colors.OKCYAN}Note: Tests preserve existing files (only use free space).{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Tip: Full capacity test fills entire drive - best for detecting fake drives{Colors.ENDC}")
    if platform.system() == 'Linux':
        print(f"{Colors.WARNING}Tip: Run with sudo for accurate read speeds (bypasses cache){Colors.ENDC}")

def interactive_mode():
    """Run in interactive menu mode"""
    os_name, os_emoji = get_platform_info()
    
    print_section(EMOJI['folder'], "Test Path Configuration")
    print_info(f"Running on {os_emoji} {os_name}")
    
    if os_name == 'Windows':
        print_info("Example: E:\\ or F:\\")
    else:
        print_info("Example: /Volumes/USB or /media/usb or /mnt/usb")
    
    test_path = input(f"\nEnter USB drive path: ").strip()
    
    if not validate_path(test_path):
        sys.exit(1)
    
    print_success(f"Using path: {test_path}")
    
    while True:
        show_menu()
        choice = input(f"{EMOJI['think']} Enter your choice: ").strip()
        
        if choice == '1':
            run_speed_tests(test_path, num_tests=5, test_size_mb=512)
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '2':
            print_info("High Performance Mode - Testing with 2GB files")
            print_warning("This test will use ~10 GB of disk space")
            run_speed_tests(test_path, num_tests=5, test_size_mb=2048)
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '3':
            run_capacity_test(test_path, test_size_gb=5)
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '4':
            # Full capacity test - use all free space
            free_gb, total_gb, used_gb = get_disk_space(test_path)
            test_size = int(free_gb - 0.5)  # Leave 500MB buffer
            print_info(f"Full Capacity Test - Will test {test_size} GB (all free space)")
            print_warning(f"This will temporarily fill the entire drive!")
            print_warning(f"Estimated time: ~{int(test_size * 2)} minutes")
            run_capacity_test(test_path, test_size_gb=test_size)
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '5':
            run_speed_tests(test_path, num_tests=5, test_size_mb=512)
            # Full capacity test for "all tests"
            free_gb, total_gb, used_gb = get_disk_space(test_path)
            test_size = int(free_gb - 0.5)
            run_capacity_test(test_path, test_size_gb=test_size)
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '6':
            try:
                num_tests = int(input("Number of test iterations (3-10): "))
                size_mb = int(input("Test size in MB (50-4096): "))
                if 3 <= num_tests <= 10 and 50 <= size_mb <= 4096:
                    run_speed_tests(test_path, num_tests=num_tests, test_size_mb=size_mb)
                else:
                    print_error("Invalid values!")
            except ValueError:
                print_error("Invalid input!")
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '7':
            try:
                print_info("Enter test size in GB, or 0 to test all free space")
                free_gb, total_gb, used_gb = get_disk_space(test_path)
                print_info(f"Available: {free_gb:.1f} GB free")
                size_gb = int(input("Test size in GB: "))
                if size_gb == 0:
                    # Test all free space
                    size_gb = int(free_gb - 0.5)
                    print_info(f"Testing all free space: {size_gb} GB")
                if size_gb >= 1 and size_gb <= free_gb:
                    run_capacity_test(test_path, test_size_gb=size_gb)
                else:
                    print_error("Invalid value! Must be 0 (all) or 1 to available space")
            except ValueError:
                print_error("Invalid input!")
            input(f"\n{EMOJI['ok']} Press Enter to continue...")
        
        elif choice == '0':
            print(f"\n{EMOJI['ok']} Goodbye!\n")
            break
        
        else:
            print_error("Invalid choice!")
            time.sleep(1)

def command_line_mode(args):
    """Run in command-line mode"""
    if not validate_path(args.path):
        sys.exit(1)
    
    if args.speed or args.all:
        iterations = args.iterations if args.iterations else 5
        # Use 2GB for fast mode, otherwise use specified size or default 512MB
        if args.size_mb:
            size_mb = args.size_mb
        elif args.fast:
            size_mb = 2048
            print_info(f"{EMOJI['fire']} High-performance mode enabled - using 2GB test files")
        else:
            size_mb = 512
        run_speed_tests(args.path, num_tests=iterations, test_size_mb=size_mb)
    
    if args.capacity or args.all:
        if args.full_capacity:
            # Test all free space
            free_gb, total_gb, used_gb = get_disk_space(args.path)
            size_gb = int(free_gb - 0.5)  # Leave 500MB buffer
            print_info(f"{EMOJI['capacity']} Full capacity test - testing {size_gb} GB (all free space)")
            print_warning("This will temporarily fill the entire drive!")
        else:
            size_gb = args.size_gb if args.size_gb else 5
        run_capacity_test(args.path, test_size_gb=size_gb)
    
    print(f"\n{EMOJI['check']} {Colors.OKGREEN}All tests completed!{Colors.ENDC}\n")

def main():
    parser = argparse.ArgumentParser(
        description=f'{EMOJI["usb"]} Cross-Platform USB Device Testing Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python test_usb.py                              # Interactive mode
  python test_usb.py -s /media/usb                # Speed test (512MB x 5)
  python test_usb.py -s /media/usb --fast         # High-performance (2GB x 5)
  python test_usb.py -c E:\\ --size-gb 5          # Quick capacity test (5GB)
  python test_usb.py -c E:\\ --full-capacity      # Full capacity test (all free space)
  python test_usb.py -a /Volumes/USB              # All tests (macOS)
  python test_usb.py -s /mnt/usb --size-mb 2048   # Custom: 2GB x 5
  python test_usb.py -s /mnt/usb -n 8 --size-mb 4096  # Custom: 4GB x 8

Test Size Guidelines:
  Speed Tests:
    - Standard (512MB):  USB 2.0, USB 3.0 drives (<500 MB/s)
    - Fast (2GB):        NVMe, Thunderbolt, fast SSDs (500-2000 MB/s)
    - Custom (4GB+):     Ultra-fast drives (>2000 MB/s)
  
  Capacity Tests:
    - Quick (5GB):       Fast verification, detects obvious fakes
    - Full (all space):  Thorough testing, best for fake drive detection

Cross-Platform Notes:
  - Works on Windows, macOS, and Linux
  - No external dependencies required
  - Pure Python implementation
  - Tests preserve existing files
  - On Linux: run with sudo for accurate read speeds (bypasses cache)
        '''
    )
    
    parser.add_argument('path', nargs='?', help='USB drive path')
    parser.add_argument('-s', '--speed', action='store_true',
                       help='Run speed test only')
    parser.add_argument('-c', '--capacity', action='store_true',
                       help='Run capacity test only')
    parser.add_argument('-a', '--all', action='store_true',
                       help='Run all tests')
    parser.add_argument('--fast', action='store_true',
                       help='High-performance mode (2GB test files for fast drives >500MB/s)')
    parser.add_argument('--full-capacity', action='store_true',
                       help='Test ALL free space (best for detecting fake drives)')
    parser.add_argument('-n', '--iterations', type=int,
                       help='Number of speed test iterations (default: 5)')
    parser.add_argument('--size-mb', type=int,
                       help='Size in MB for speed test (default: 512, or 2048 with --fast)')
    parser.add_argument('--size-gb', type=int,
                       help='Size in GB for capacity test (default: 5, ignored with --full-capacity)')
    parser.add_argument('--no-interactive', action='store_true',
                       help='Disable interactive mode')
    
    args = parser.parse_args()
    
    # Show platform info
    os_name, os_emoji = get_platform_info()
    print_header(f"{os_emoji} Cross-Platform USB Tester - {os_name}")
    
    # Run appropriate mode
    if not args.path and not args.no_interactive:
        interactive_mode()
    elif args.path:
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
        import traceback
        traceback.print_exc()
        sys.exit(1)
