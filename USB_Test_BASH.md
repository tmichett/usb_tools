# USB Test BASH Script Documentation

## Overview

`usb_test.sh` is a comprehensive USB drive testing utility that evaluates both the **speed** and **capacity** of USB storage devices. It helps detect fake/counterfeit USB drives and measures actual read/write performance.

## Features

- **Speed Testing**: Measures sequential read and write speeds using `fio` (Flexible I/O Tester)
- **Capacity Testing**: Validates actual storage capacity and detects fake drives using `f3` (Fight Flash Fraud)
- **Flexible Modes**: Run tests individually or combined
- **Clean Automation**: Automatic cleanup of test files

## System Requirements

### Operating System
- Linux-based systems (tested on Fedora, Ubuntu, Debian, and derivatives)
- Bash shell

### Required Packages

The script requires the following tools to be installed:

1. **fio** - Flexible I/O Tester for speed benchmarking
2. **f3** - Fight Flash Fraud tools (includes `f3write`, `f3read`, and `f3probe`)
3. **awk** - Text processing (usually pre-installed)
4. **sed** - Stream editor (usually pre-installed)

**Note**: `f3probe` (included in newer f3 packages) is optional but recommended for non-destructive capacity testing. The script will work without it, but you'll only have access to the destructive capacity test.

### Installation Instructions

#### Fedora / RHEL / CentOS
```bash
sudo dnf install fio f3
```

#### Ubuntu / Debian / Linux Mint
```bash
sudo apt install fio f3
```

#### Arch Linux
```bash
sudo pacman -S fio f3
```

#### openSUSE
```bash
sudo zypper install fio f3
```

## Usage

### Basic Syntax
```bash
sudo ./usb_test.sh [OPTION] [MOUNT_POINT]
```

**Important**: The script must be run with `sudo` (root privileges) because:
- Direct I/O operations require elevated permissions
- Writing large test files to the USB drive requires proper access

### Command Options

| Option | Description |
|--------|-------------|
| `-s` | Speed Test Only - Measures read/write speeds |
| `-p` | Capacity Test (Non-Destructive) - Tests free space only using f3probe |
| `-c` | Capacity Test (Full/Destructive) - Validates entire drive capacity |
| `-a` | All Tests - Runs speed and full capacity tests |
| `-h` | Show help message |

### Examples

#### 1. Run Speed Test Only
```bash
sudo ./usb_test.sh -s /media/usb
```
This performs a 512MB read/write test and reports speeds in MiB/s.

#### 2. Run Non-Destructive Capacity Test
```bash
sudo ./usb_test.sh -p /media/usb
```
This tests the free space on your drive without touching existing files. Safe and fast!

**✅ Safe**: Your existing files will NOT be touched. Only free space is tested.

#### 3. Run Full Capacity Test (Destructive)
```bash
sudo ./usb_test.sh -c /media/usb
```
This writes test files across the entire drive, then reads them back to verify integrity.

**⚠️ Warning**: This test will fill the entire USB drive with test data. Any existing data will be overwritten!

#### 4. Run All Tests
```bash
sudo ./usb_test.sh -a /media/usb
```
Runs both speed and full capacity tests sequentially.

## Capacity Testing: Destructive vs Non-Destructive

### Non-Destructive Capacity Test (`-p`)

**What it does**:
- Uses `f3probe` to test only the FREE SPACE on your drive
- Does NOT touch or delete existing files
- Faster than full capacity test
- Safe to run on drives with important data

**When to use**:
- Testing a drive that already has files you want to keep
- Quick capacity verification
- Checking for obvious capacity fraud

**Limitations**:
- Only tests free space, not the entire drive
- May miss issues in areas where existing files are stored
- Less comprehensive than full capacity test

### Full Capacity Test (`-c`)

**What it does**:
- Uses `f3write` and `f3read` to test the ENTIRE drive
- Fills the drive completely with test data
- Reads back and verifies every byte
- Most thorough test for detecting fake drives

**When to use**:
- Testing a brand new USB drive
- Suspicious drives that may be counterfeit
- When you need the most comprehensive test
- After backing up important data

**⚠️ Warning**:
- **DESTRUCTIVE** - Erases all data on the drive
- Takes several hours on large drives
- Always backup first!

## How It Works

### Speed Test (`-s`)

1. Creates a 512MB test file on the USB drive
2. Uses `fio` with direct I/O to bypass system caching
3. Performs sequential read and write operations with 1MB block size
4. Parses and displays the results in MiB/s
5. Automatically cleans up test files

**Test Parameters**:
- Block Size: 1MB
- Test File Size: 512MB
- I/O Pattern: Sequential read/write
- Direct I/O: Enabled (bypasses cache)

### Capacity Test (`-c`)

1. Uses `f3write` to fill the drive with test data
2. Uses `f3read` to read back and verify data integrity
3. Detects fake drives that report incorrect capacity
4. Automatically cleans up `.h2w` test files

**⚠️ Important Notes**:
- This test is **destructive** - it overwrites existing data
- Test duration depends on drive size (can take hours for large drives)
- Backup any important data before running this test

## Output Examples

### Speed Test Output
```
>>> RUNNING SPEED TEST <<<
---------------------------------------
  Read Speed  : 145.23 MiB/s
  Write Speed : 98.67 MiB/s
---------------------------------------
```

### Capacity Test Output
```
>>> RUNNING CAPACITY TEST (f3) <<<
Free space: 14.90 GB
Creating file 1.h2w ... OK!
Creating file 2.h2w ... OK!
...
Data OK: 14.90 GB (31242240 sectors)
```

## Troubleshooting

### Error: Command not found
```
Error: fio is not installed. Please run: sudo apt install fio f3
```
**Solution**: Install the required packages using your distribution's package manager.

### Permission Denied
**Solution**: Ensure you're running the script with `sudo`:
```bash
sudo ./usb_test.sh -s /media/usb
```

### Invalid Mount Point
**Solution**: Verify the USB drive is mounted:
```bash
lsblk
mount | grep /media
```

### Script Not Executable
**Solution**: Make the script executable:
```bash
chmod +x usb_test.sh
```

## Understanding Test Results

### Speed Test Interpretation
- **USB 2.0**: Theoretical max ~60 MB/s (practical ~30-40 MB/s)
- **USB 3.0**: Theoretical max ~625 MB/s (practical ~100-400 MB/s)
- **USB 3.1**: Theoretical max ~1250 MB/s (practical ~500-900 MB/s)
- **USB 3.2**: Theoretical max ~2500 MB/s (practical ~1000-2000 MB/s)

Lower speeds may indicate:
- Older USB standard
- Poor quality drive
- Faulty hardware
- USB port limitations

### Capacity Test Interpretation
- **All sectors OK**: Drive is genuine and working properly
- **Data corruption detected**: Drive may be failing or fake
- **Fewer sectors than advertised**: Counterfeit drive with misreported capacity

## Best Practices

1. **Backup First**: Always backup data before running capacity tests
2. **Unmount After**: Safely unmount the drive after testing
3. **Check Results**: Compare speeds against manufacturer specifications
4. **Regular Testing**: Test new USB drives immediately after purchase
5. **Port Selection**: Use USB 3.0+ ports for accurate speed testing

## Technical Details

### Dependencies Check
The script automatically verifies all required tools are installed before running any tests. If a dependency is missing, it provides installation instructions and exits gracefully.

### Cleanup
All test files are automatically removed after testing:
- Speed test: Removes `fio_test.tmp` and `/tmp/fio_results.txt`
- Capacity test: Removes all `*.h2w` files

### Direct I/O
The speed test uses direct I/O (`--direct=1`) to bypass the system's page cache, ensuring accurate measurements of the USB drive's actual performance rather than RAM speeds.

## Security Considerations

- **Root Privileges**: Required for direct I/O operations
- **Data Destruction**: Capacity tests will overwrite all data on the drive
- **Temporary Files**: Created in `/tmp` directory, cleaned up automatically

## License

This script is provided as-is for USB drive testing and validation purposes.

## Support

For issues or questions:
1. Verify all dependencies are installed
2. Check that the USB drive is properly mounted
3. Ensure you have root/sudo privileges
4. Review error messages for specific guidance

---

**Version**: 1.0  
**Last Updated**: January 2026
