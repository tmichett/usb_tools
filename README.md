# USB Tools 💾

Comprehensive USB drive testing utilities for Linux systems. Test drive speed and validate capacity to detect fake/counterfeit USB drives.

## 📦 Available Tools

### 1. **usb_test.py** - Python Testing Suite (Recommended)
Modern Python-based USB testing tool with:
- 🎨 Interactive menu system
- 📊 Multiple speed test iterations with statistics
- 🛡️ Quick capacity test option (5 GB, ~10-20 min)
- 📦 Full capacity test option (all free space, thorough)
- ✅ Preserves existing files on your drive
- 🌈 Beautiful Unicode/emoji output
- 📈 Advanced performance analysis
- ⚡ More robust testing capabilities

### 2. **usb_test.sh** - Bash Script (Legacy)
Original bash script for quick testing:
- Simple command-line interface
- Fast single-pass speed tests
- Full capacity testing with f3write/f3read
- Preserves existing files
- Capacity validation and fake drive detection

## 🚀 Quick Start

### Python Version (Interactive)
```bash
sudo python3 usb_test.py
```

### Python Version (Command Line)
```bash
# Speed test only
sudo python3 usb_test.py -s /media/usb

# Quick capacity test (5 GB, ~10-20 min)
sudo python3 usb_test.py -q /media/usb

# Full capacity test (all free space, hours)
sudo python3 usb_test.py -c /media/usb

# All tests (speed + full capacity)
sudo python3 usb_test.py -a /media/usb

# Custom iterations
sudo python3 usb_test.py -s /media/usb -n 8
```

### Bash Version
```bash
# Speed test only
sudo ./usb_test.sh -s /media/usb

# Capacity test (fills all free space, preserves files)
sudo ./usb_test.sh -c /media/usb

# All tests (speed + capacity)
sudo ./usb_test.sh -a /media/usb
```

## 📋 System Requirements

### Required Packages
- **fio** - Flexible I/O Tester
- **f3** - Fight Flash Fraud tools
- **python3** - For the Python version (usually pre-installed)

### Installation

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install fio f3 python3
```

**Ubuntu/Debian:**
```bash
sudo apt install fio f3 python3
```

**Arch Linux:**
```bash
sudo pacman -S fio f3 python
```

## 📚 Documentation

- [**USB_Test_BASH.md**](USB_Test_BASH.md) - Detailed bash script documentation
- [**USB_Test_PYTHON.md**](USB_Test_PYTHON.md) - Python script guide and features

## ⚡ Features Comparison

| Feature | Python Script | Bash Script |
|---------|--------------|-------------|
| Interactive Menu | ✅ | ❌ |
| Multiple Test Iterations | ✅ | ❌ |
| Statistics (avg/min/max) | ✅ | ❌ |
| Unicode/Emoji Output | ✅ | ❌ |
| USB Version Detection | ✅ | ❌ |
| Performance Rating | ✅ | ❌ |
| Colored Output | ✅ | ❌ |
| Progress Indicators | ✅ | ❌ |
| Command-line Mode | ✅ | ✅ |
| Speed Test | ✅ | ✅ |
| Quick Capacity Test (limited data) | ✅ | ❌ |
| Full Capacity Test (f3write/f3read) | ✅ | ✅ |
| Preserves Existing Files | ✅ | ✅ |

## 🎯 Use Cases

- **Verify new USB drives** - Detect counterfeit/fake capacity drives
- **Performance testing** - Measure actual read/write speeds
- **Quality assurance** - Test drive reliability over multiple runs
- **Troubleshooting** - Identify slow or failing drives
- **Purchase validation** - Verify advertised specifications

## ⚠️ Important Notes

- **Root required**: Both scripts require sudo/root privileges
- **Capacity tests preserve files**: Tests fill free space but do NOT delete existing files
- **Python offers two modes**:
  - 🛡️ **Quick test** (`-q`): Tests 5 GB, fast (~10-20 min)
  - 📦 **Full test** (`-c`): Tests all free space, thorough (hours)
- **Bash has one mode**: Full capacity test using f3write/f3read
- **Time required**: Full tests take hours on large drives, quick tests finish in minutes

## 🤝 Contributing

Feel free to submit issues or pull requests for improvements!

## 📄 License

These tools are provided as-is for USB drive testing and validation purposes.
