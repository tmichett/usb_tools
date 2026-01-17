# USB Test Python Script Documentation 💾

## Overview

`usb_test.py` is a modern, feature-rich Python implementation of the USB testing suite. It provides an interactive menu system, multiple test iterations with statistical analysis, and beautiful Unicode/emoji output for an enhanced user experience.

## ✨ Key Features

### 🎨 User Interface
- **Interactive Menu System** - Easy-to-use numbered menu interface
- **Unicode & Emoji Support** - Visual indicators and beautiful output
- **Color-Coded Output** - ANSI colors for different message types
- **Progress Indicators** - Real-time feedback during tests

### 📊 Advanced Testing
- **Multiple Speed Test Iterations** - Run 3-10 tests and average results
- **Statistical Analysis** - Average, min, max, and standard deviation
- **USB Version Detection** - Automatic identification of USB 2.0/3.0/3.1/3.2
- **Performance Rating** - Qualitative assessment of drive performance

### 🛠️ Flexibility
- **Interactive Mode** - Menu-driven interface
- **Command-Line Mode** - Script-friendly batch operations
- **Customizable Iterations** - Choose how many speed tests to run
- **Comprehensive Error Handling** - Graceful failure and cleanup

## 🖥️ System Requirements

### Operating System
- Linux-based systems (Fedora, Ubuntu, Debian, Arch, etc.)
- Python 3.6 or higher

### Required Packages

1. **Python 3** - Usually pre-installed on modern Linux systems
2. **fio** - Flexible I/O Tester for speed benchmarking
3. **f3** - Fight Flash Fraud tools (includes f3write and f3read)

### Python Standard Library Dependencies
All required Python modules are part of the standard library:
- `os`, `sys`, `subprocess`, `argparse`, `json`, `tempfile`, `re`, `shutil`
- `pathlib`, `statistics`, `time`

No additional pip packages are required! 🎉

### Installation Commands

#### Fedora / RHEL / CentOS
```bash
sudo dnf install python3 fio f3
```

#### Ubuntu / Debian / Linux Mint
```bash
sudo apt install python3 fio f3
```

#### Arch Linux
```bash
sudo pacman -S python fio f3
```

#### openSUSE
```bash
sudo zypper install python3 fio f3
```

## 📖 Usage

### Interactive Mode (Recommended)

Simply run the script without arguments to enter interactive mode:

```bash
sudo python3 usb_test.py
```

**Interactive Mode Features:**
1. Guided mount point input
2. Menu-based test selection
3. Custom iteration configuration
4. Confirmation prompts for destructive operations
5. Easy navigation and repeatable tests

**Menu Options:**
```
1. ⚡ Speed Test Only
2. 📦 Capacity Test Only
3. 🚀 Run All Tests
4. ⚙️  Advanced Speed Test (custom iterations)
0. ❌ Exit
```

### Command-Line Mode

For automation and scripting, use command-line arguments:

#### Basic Syntax
```bash
sudo python3 usb_test.py [OPTIONS] <MOUNT_POINT>
```

#### Options

| Option | Description |
|--------|-------------|
| `-s, --speed` | Run speed test only |
| `-c, --capacity` | Run capacity test only |
| `-a, --all` | Run all tests |
| `-n, --iterations N` | Number of speed test iterations (default: 5) |
| `--no-interactive` | Disable interactive mode |
| `-h, --help` | Show help message |

### Examples

#### 1. Interactive Mode
```bash
sudo python3 usb_test.py
```
Launches the interactive menu system.

#### 2. Speed Test with Default Iterations (5)
```bash
sudo python3 usb_test.py -s /media/usb
```
Runs 5 speed tests and displays statistics.

#### 3. Speed Test with Custom Iterations
```bash
sudo python3 usb_test.py -s /media/usb -n 8
```
Runs 8 speed tests for more accurate averaging.

#### 4. Capacity Test Only
```bash
sudo python3 usb_test.py -c /media/usb
```
Validates the drive's actual storage capacity.

**⚠️ Warning**: Capacity test is destructive and will overwrite all data!

#### 5. Run All Tests
```bash
sudo python3 usb_test.py -a /media/usb
```
Runs both speed tests and capacity tests.

#### 6. Quick 3-Iteration Speed Test
```bash
sudo python3 usb_test.py -s /media/usb -n 3
```
Faster testing with 3 iterations instead of 5.

## 🔬 How It Works

### Speed Testing

The Python version improves upon the bash script by running **multiple test iterations**:

1. **Initialization**
   - Validates mount point
   - Checks available disk space
   - Prepares test environment

2. **Test Execution** (repeated N times)
   - Creates 512MB test file on USB drive
   - Uses `fio` with direct I/O (bypasses cache)
   - Performs sequential read/write with 1MB blocks
   - Parses JSON output from fio
   - Cleans up test files

3. **Statistical Analysis**
   - Calculates average read/write speeds
   - Determines minimum and maximum speeds
   - Computes standard deviation
   - Identifies outliers

4. **Results Presentation**
   - Displays all individual test results
   - Shows comprehensive statistics
   - Estimates USB version (2.0/3.0/3.1/3.2)
   - Provides performance rating

**Test Parameters:**
- Block Size: 1MB
- Test File Size: 512MB per iteration
- I/O Pattern: Sequential read/write
- Direct I/O: Enabled (bypasses cache)
- Default Iterations: 5 (customizable)

### Capacity Testing

Identical to the bash version but with enhanced UI:

1. **User Confirmation**
   - Warns about data loss
   - Requires explicit confirmation

2. **Write Phase** (`f3write`)
   - Fills entire drive with test data
   - Creates numbered .h2w files

3. **Read Phase** (`f3read`)
   - Reads back all test data
   - Verifies data integrity
   - Detects fake capacity

4. **Cleanup**
   - Automatically removes all .h2w test files
   - Reports number of files cleaned

## 📊 Understanding Results

### Speed Test Output Example

```
📊 Speed Test Results
───────────────────────────────────────────────

📖 READ PERFORMANCE:
  Average: 145.67 MB/s
  Maximum: 152.34 MB/s
  Minimum: 141.23 MB/s
  Std Dev: 3.89 MB/s

✍️  WRITE PERFORMANCE:
  Average: 98.45 MB/s
  Maximum: 102.11 MB/s
  Minimum: 95.78 MB/s
  Std Dev: 2.34 MB/s

🔌 USB VERSION ESTIMATE:
  🚀 USB 3.0 / 3.1 Gen 1

⭐ PERFORMANCE RATING:
  👍 Good performance
```

### Performance Ratings

| Rating | Read Speed | Write Speed | Indicator |
|--------|-----------|-------------|-----------|
| Excellent | >100 MB/s | >100 MB/s | 🔥 |
| Good | >50 MB/s | >50 MB/s | 👍 |
| Moderate | >20 MB/s | >20 MB/s | 🤔 |
| Poor | <20 MB/s | <20 MB/s | ⚠️ |

### USB Version Detection

Based on the highest average speed (read or write):

| Max Speed | USB Version | Theoretical Max |
|-----------|-------------|-----------------|
| <50 MB/s | USB 2.0 | 60 MB/s |
| 50-450 MB/s | USB 3.0 / 3.1 Gen 1 | 625 MB/s |
| 450-1000 MB/s | USB 3.1 Gen 2 | 1250 MB/s |
| >1000 MB/s | USB 3.2+ | 2500+ MB/s |

### Statistical Significance

- **Standard Deviation**: Measures consistency across tests
  - Low (<5 MB/s): Consistent, reliable performance
  - Medium (5-15 MB/s): Normal variation
  - High (>15 MB/s): Inconsistent, possible issues

- **Min/Max Range**: Shows performance variation
  - Narrow range: Stable drive
  - Wide range: Performance fluctuations

## 🎨 Visual Elements

### Emoji Legend

| Emoji | Meaning | Usage |
|-------|---------|-------|
| 💾 | USB Drive | Headers, drive references |
| ⚡ | Speed | Speed test options |
| 📦 | Capacity | Capacity test options |
| ✅ | Success | Successful operations |
| ❌ | Error | Failed operations |
| ⚠️ | Warning | Important warnings |
| 📊 | Statistics | Results display |
| 🚀 | Fast | High performance |
| 🔥 | Excellent | Outstanding performance |
| 👍 | Good | Satisfactory results |
| 🤔 | Moderate | Average performance |
| 🧹 | Cleanup | File removal |
| ⚙️ | Settings | Configuration |

### Color Coding

- **Green** (✅): Success messages, good performance
- **Blue** (ℹ️): Informational messages, maximum values
- **Yellow** (⚠️): Warnings, minimum values
- **Red** (❌): Errors, failures
- **Cyan**: Section headers, test progress

## 🛠️ Troubleshooting

### Common Issues

#### 1. Permission Denied
```
❌ This script requires root privileges!
```
**Solution**: Run with sudo
```bash
sudo python3 usb_test.py
```

#### 2. Dependencies Missing
```
❌ Flexible I/O Tester (fio) - Not Found
```
**Solution**: Install required packages
```bash
sudo apt install fio f3  # Debian/Ubuntu
sudo dnf install fio f3  # Fedora/RHEL
```

#### 3. Mount Point Invalid
```
❌ Mount point does not exist: /media/usb
```
**Solution**: Verify the USB drive is mounted
```bash
lsblk
mount | grep /media
```
Or use `df -h` to find the correct mount point.

#### 4. Not Enough Space for Speed Test
Speed tests require at least 512MB of free space.

**Solution**: Free up space or the script will fail gracefully.

#### 5. Python Version Too Old
The script requires Python 3.6 or higher.

**Solution**: Update Python
```bash
python3 --version  # Check version
sudo apt install python3  # Update if needed
```

### Script Interruption

Press `Ctrl+C` to interrupt any test:
- Speed tests: Cleanup is automatic
- Capacity tests: Asks for confirmation, then cleans up .h2w files

## 💡 Best Practices

### 1. Testing Strategy
- **New Drives**: Run all tests to verify authenticity
- **Performance Check**: Use speed test with 5+ iterations
- **Quick Test**: Use speed test with 3 iterations
- **Fake Detection**: Always run capacity test on new drives

### 2. Accuracy Tips
- Close other applications during testing
- Use USB 3.0+ ports for USB 3.0+ drives
- Avoid USB hubs when possible
- Run multiple iterations (5-8) for accurate averages
- Test at different times to account for thermal throttling

### 3. Safety
- **Always backup** before capacity tests
- Verify mount point before testing
- Don't interrupt capacity tests unnecessarily
- Safely eject drive after testing

### 4. Interpreting Results
- Compare speeds with manufacturer specifications
- Consider USB port limitations
- Account for drive age and wear
- Look for consistency across iterations

## 🔧 Advanced Usage

### Custom Test Sizes

To modify test file size, edit the script:
```python
# Line ~225 in run_speed_test()
run_single_speed_test(mount_point, test_size_mb=1024)  # 1GB test
```

### Adjusting Timeout

For very slow drives, increase timeout:
```python
# Line ~164 in run_single_speed_test()
result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # 10 min
```

### Batch Testing Multiple Drives

Create a wrapper script:
```bash
#!/bin/bash
for drive in /media/usb1 /media/usb2 /media/usb3; do
    echo "Testing $drive"
    sudo python3 usb_test.py -s "$drive" -n 5
done
```

## 🆚 Comparison with Bash Version

### Advantages of Python Version

1. **Statistical Analysis**: Multiple iterations with avg/min/max/stdev
2. **Better UX**: Interactive menu, colors, emojis
3. **USB Detection**: Automatically identifies USB version
4. **Performance Rating**: Qualitative assessment
5. **Error Handling**: More robust error detection and recovery
6. **Extensibility**: Easier to modify and extend
7. **Cross-platform Ready**: Easier to port to other systems

### When to Use Bash Version

- Minimal dependencies desired
- Scripting in pure bash environments
- Single quick test needed
- Legacy system compatibility

## 🐛 Known Limitations

1. **Linux Only**: Uses Linux-specific tools (fio, f3)
2. **Root Required**: Needs sudo for direct I/O
3. **Test Duration**: Multiple iterations take longer
4. **Disk Space**: Requires 512MB × iterations for speed tests

## 📝 Version History

- **v1.0** (January 2026)
  - Initial Python implementation
  - Interactive menu system
  - Multiple iteration support
  - Statistical analysis
  - Unicode/emoji output
  - USB version detection
  - Performance rating

## 🤝 Contributing

Suggestions for improvements:
- Additional test patterns (random I/O)
- GUI version
- Cross-platform support (Windows, macOS)
- Configuration file support
- Test result logging to file
- Benchmark database comparison

## 📄 License

This script is provided as-is for USB drive testing and validation purposes.

## 🆘 Support

If you encounter issues:
1. Verify all dependencies are installed
2. Check USB drive is properly mounted
3. Ensure sufficient free space
4. Confirm running with sudo
5. Review error messages carefully

---

**Created**: January 2026  
**Author**: USB Tools Project  
**Version**: 1.0
